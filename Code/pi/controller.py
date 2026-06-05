import pygame
import pygame.gfxdraw

import config as config

joysticks = []
axis_motion = [0, 0, 0, 0, -1, -1]  # left x, left y, right x, right y, left trigger, right trigger

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
		if event.type == pygame.JOYDEVICEADDED:
			on_device_added(event.device_index)
		if event.type == pygame.JOYDEVICEREMOVED:
			on_device_removed(event.instance_id)
		if event.type == pygame.JOYAXISMOTION:
			on_axis_motion(event.axis, event.value)
			result["needs_update"] = True
		if event.type == pygame.JOYBUTTONUP:
			if event.button == config.RS_BTN:
				result["toggle_draw"] = True
			if event.button == config.B_BTN:
				config.curr_right_multiplier += 0.01
			if event.button == config.X_BTN:
				config.curr_right_multiplier -= 0.01

	for joy in joysticks:
		if joy.get_button(config.SELECT_BTN) and joy.get_button(config.START_BTN):
			result["close"] = True
		if handle_speed_change(joy): result["needs_update"] = True

	return result

def on_axis_motion(axis, value):
	axis_motion[axis] = value
	sanitize_joy_input()
	#print(axis_motion)

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
	left_y  = int(half_height + round(axis_motion[1] * (JOY_CIRCLE_RADIUS / JOY_DIV)))
	right_x = int(third_width * 2 + round(axis_motion[2] * (JOY_CIRCLE_RADIUS / JOY_DIV)))
	right_y = int(half_height + round(axis_motion[3] * (JOY_CIRCLE_RADIUS / JOY_DIV)))

	pygame.gfxdraw.filled_circle(screen, left_x, left_y, JOY_CIRCLE_RADIUS // 2, (255, 255, 255))
	pygame.gfxdraw.filled_circle(screen, right_x, right_y, JOY_CIRCLE_RADIUS // 2, (255, 255, 255))
