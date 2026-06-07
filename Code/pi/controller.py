import pygame
import pygame.gfxdraw

import config as config
import helpers as helpers

joysticks = []
axis_motion = [0, 0, 0, 0, -1, -1]  # left x, left y, right x, right y, left trigger, right trigger
drivetrain = [0, 0]

JOY_CIRCLE_RADIUS = 100
JOY_DIV = 1.5  # smaller = more inner circle movement relative to outer

def init():
	pygame.joystick.init()
	for i in range(pygame.joystick.get_count()):
		joysticks.append(pygame.joystick.Joystick(i))

def on_device_added(device_index):
	joysticks.append(pygame.joystick.Joystick(device_index))

def on_device_removed(instance_id):
	global joysticks
	joysticks = [j for j in joysticks if j.get_instance_id() != instance_id]

def handle_input(events):
	result = {"needs_update": False, "close": False, "toggle_draw": False}

	for event in events:
		if event.type == pygame.JOYDEVICEADDED: # Add controller
			on_device_added(event.device_index)
		if event.type == pygame.JOYDEVICEREMOVED: # Remove controller
			on_device_removed(event.instance_id)
		if event.type == pygame.JOYAXISMOTION: # Joy or trigger update
			on_axis_motion(event.axis, event.value)
			result["needs_update"] = True

		if event.type == pygame.JOYBUTTONUP: # Button up
			if event.button == config.RS_BTN: # Right stick pressed
				result["toggle_draw"] = True
			if event.button == config.LS_BTN: # Left stick pressed
				if config.curr_control_mode == config.ControlMode.DUAL_JOY:
					config.curr_control_mode = config.ControlMode.SINGLE_JOY
				else:
					config.curr_control_mode = config.ControlMode.DUAL_JOY
			if event.button == config.B_BTN: # B button pressed
				config.curr_right_multiplier += 0.01
				config.curr_right_multiplier = helpers.clamp(config.curr_right_multiplier, 0, 1)
			if event.button == config.X_BTN: # X button pressed
				config.curr_right_multiplier -= 0.01
				config.curr_right_multiplier = helpers.clamp(config.curr_right_multiplier, 0, 1)

	for joy in joysticks:
		if joy.get_button(config.SELECT_BTN) and joy.get_button(config.START_BTN):
			result["close"] = True
		if handle_speed_change(joy): result["needs_update"] = True

	return result

def on_axis_motion(axis, value):
	if axis == 1 or axis == 3:  # flip Y axes once at ingestion so up = +1, down = -1
		value = -value
	axis_motion[axis] = value
	sanitize_joy_input()
	if config.curr_control_mode == config.ControlMode.DUAL_JOY:
		drivetrain[0] = axis_motion[1]
		drivetrain[1] = axis_motion[3]
	else:
		handle_single_joy()
	#print(axis_motion, " | ",  drivetrain)
	

def handle_single_joy():
	throttle = axis_motion[1]  # +1 = forward (Y already flipped in on_axis_motion)
	turn = axis_motion[0]

	left = throttle + turn
	right = throttle - turn

	# scale both sides down together when either exceeds 1 so the turn
	# ratio is preserved instead of one side clipping at full throttle
	m = max(1.0, abs(left), abs(right))
	drivetrain[0] = round(left / m, 2)
	drivetrain[1] = round(right / m, 2)

def handle_speed_change(joy):
	if joy.get_button(config.LB_BUTTON):
		config.curr_max_speed -= config.SPEED_CHANGE
		if config.curr_max_speed < config.MIN_SPEED: config.curr_max_speed = config.MIN_SPEED
	elif joy.get_button(config.RB_BTN):
		config.curr_max_speed += config.SPEED_CHANGE
		if config.curr_max_speed > config.MAX_SPEED: config.curr_max_speed = config.MAX_SPEED
	else:
		return False
	config.curr_max_speed = round(config.curr_max_speed, 2)
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
