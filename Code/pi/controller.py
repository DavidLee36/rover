import pygame
import pygame.gfxdraw
from pygame._sdl2 import controller as sdl_controller

import config as config
import controller_mapping as cmap
import helpers as helpers
import state as state

controllers = {}  # instance_id -> sdl_controller.Controller
axis_motion = [0, 0, 0, 0, 0, 0]  # left x, left y, right x, right y, left trigger, right trigger
drivetrain = [0, 0]

JOY_CIRCLE_RADIUS = 100
JOY_DIV = 1.5  # smaller = more inner circle movement relative to outer

def init():
	sdl_controller.init()
	try:
		sdl_controller.set_eventstate(True)  # ensure CONTROLLER* events are emitted
	except Exception:
		pass  # not present on this pygame build
	for i in range(sdl_controller.get_count()):  # open any already-connected pad
		if sdl_controller.is_controller(i):
			open_controller(i)

def open_controller(device_index):
	c = sdl_controller.Controller(device_index)
	# CONTROLLERDEVICEREMOVED / button / axis events report instance_id, so key
	# by that (device_index is a separate, add-time-only namespace).
	controllers[c.as_joystick().get_instance_id()] = c

def on_device_added(device_index):
	open_controller(device_index)

def on_device_removed(instance_id):
	controllers.pop(instance_id, None)

def handle_input(events):
	result = {"needs_update": False, "close": False, "toggle_draw": False, "toggle_ctrl_mode": False}

	for event in events:
		if event.type == pygame.CONTROLLERDEVICEADDED: # Add controller
			on_device_added(event.device_index)
		if event.type == pygame.CONTROLLERDEVICEREMOVED: # Remove controller
			on_device_removed(event.instance_id)
		if event.type == pygame.CONTROLLERAXISMOTION: # Joy or trigger update
			on_axis_motion(event.axis, event.value)
			result["needs_update"] = True

		if event.type == pygame.CONTROLLERBUTTONUP: # Button up
			if event.button == cmap.RS_BTN: # Right stick pressed
				result["toggle_draw"] = True
			if event.button == cmap.LS_BTN: # Left stick pressed
				result["toggle_ctrl_mode"] = True
			if event.button == cmap.B_BTN: # B button pressed
				state.curr_right_multiplier += 0.01
				state.curr_right_multiplier = helpers.clamp(state.curr_right_multiplier, 0, 1)
			if event.button == cmap.X_BTN: # X button pressed
				state.curr_right_multiplier -= 0.01
				state.curr_right_multiplier = helpers.clamp(state.curr_right_multiplier, 0, 1)

	for ctrl in controllers.values():
		if ctrl.get_button(cmap.SELECT_BTN) and ctrl.get_button(cmap.START_BTN):
			result["close"] = True
		if handle_speed_change(ctrl): result["needs_update"] = True

	return result

def on_axis_motion(axis, value):
	value = value / cmap.AXIS_MAX  # SDL gives ints; normalize to ~-1..1 (triggers 0..1)
	if axis == cmap.LEFT_Y or axis == cmap.RIGHT_Y:  # flip Y axes so up = +1, down = -1
		value = -value
	axis_motion[axis] = value
	sanitize_joy_input()
	if state.curr_ctrl_mode == state.ControlMode.DUAL_JOY:
		drivetrain[0] = axis_motion[1]
		drivetrain[1] = axis_motion[3]
	else:
		handle_single_joy()
	#print(axis_motion, " | ",  drivetrain)


def handle_single_joy():
	throttle = axis_motion[1]
	turn = axis_motion[0]

	if throttle < 0:  # in reverse, flip steering
		turn = -turn

	left = throttle + turn
	right = throttle - turn

	# scale both sides down together when either exceeds 1 so the turn
	# ratio is preserved instead of one side clipping at full throttle
	m = max(1.0, abs(left), abs(right))
	drivetrain[0] = round(left / m, 2)
	drivetrain[1] = round(right / m, 2)

def handle_speed_change(ctrl):
	if ctrl.get_button(cmap.LB_BTN):
		state.curr_max_speed -= config.SPEED_CHANGE
		if state.curr_max_speed < config.MIN_SPEED: state.curr_max_speed = config.MIN_SPEED
	elif ctrl.get_button(cmap.RB_BTN):
		state.curr_max_speed += config.SPEED_CHANGE
		if state.curr_max_speed > config.MAX_SPEED: state.curr_max_speed = config.MAX_SPEED
	else:
		return False
	state.curr_max_speed = round(state.curr_max_speed, 2)
	return True

def sanitize_joy_input():
	for i in range(len(axis_motion)):
		if i <= 3 and abs(axis_motion[i]) <= 0.12:  # dead zone on joysticks
			axis_motion[i] = 0
		axis_motion[i] = max(-1, min(1, axis_motion[i]))  # clamp -1 to 1
		axis_motion[i] = round(axis_motion[i], 2)

def draw(screen):
	draw_joy_circles(screen)

def draw_joy_circles(screen):
	third_width = screen.get_width() // 3
	half_height = screen.get_height() // 2

	pygame.gfxdraw.circle(screen, third_width, half_height, JOY_CIRCLE_RADIUS, (255, 255, 255))
	pygame.gfxdraw.circle(screen, third_width * 2, half_height, JOY_CIRCLE_RADIUS, (255, 255, 255))

	left_x  = int(third_width + round(axis_motion[0] * (JOY_CIRCLE_RADIUS / JOY_DIV)))
	left_y  = int(half_height - round(axis_motion[1] * (JOY_CIRCLE_RADIUS / JOY_DIV)))
	right_x = int(third_width * 2 + round(axis_motion[2] * (JOY_CIRCLE_RADIUS / JOY_DIV)))
	right_y = int(half_height - round(axis_motion[3] * (JOY_CIRCLE_RADIUS / JOY_DIV)))

	pygame.gfxdraw.filled_circle(screen, left_x, left_y, JOY_CIRCLE_RADIUS // 2, (255, 255, 255))
	pygame.gfxdraw.filled_circle(screen, right_x, right_y, JOY_CIRCLE_RADIUS // 2, (255, 255, 255))
