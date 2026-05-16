import pygame
import pygame.gfxdraw

import config

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

def on_axis_motion(axis, value):
	axis_motion[axis] = value
	sanitize_axis_input()
	print(axis_motion)

def sanitize_axis_input():
	for i in range(len(axis_motion)):
		if i <= 3 and abs(axis_motion[i]) <= 0.12:  # dead zone on joysticks
			axis_motion[i] = 0
		axis_motion[i] = max(-1, min(1, axis_motion[i]))  # clamp -1 to 1
		axis_motion[i] = round(axis_motion[i], 2)

def draw(screen):
	draw_joy_circles(screen)

def draw_joy_circles(screen):
	third_width = config.SCREEN_WIDTH // 3
	half_height = config.SCREEN_HEIGHT // 2

	pygame.gfxdraw.circle(screen, third_width, half_height, JOY_CIRCLE_RADIUS, (255, 255, 255))
	pygame.gfxdraw.circle(screen, third_width * 2, half_height, JOY_CIRCLE_RADIUS, (255, 255, 255))

	left_x  = int(third_width + round(axis_motion[0] * (JOY_CIRCLE_RADIUS / JOY_DIV)))
	left_y  = int(half_height + round(axis_motion[1] * (JOY_CIRCLE_RADIUS / JOY_DIV)))
	right_x = int(third_width * 2 + round(axis_motion[2] * (JOY_CIRCLE_RADIUS / JOY_DIV)))
	right_y = int(half_height + round(axis_motion[3] * (JOY_CIRCLE_RADIUS / JOY_DIV)))

	pygame.gfxdraw.filled_circle(screen, left_x, left_y, JOY_CIRCLE_RADIUS // 2, (255, 255, 255))
	pygame.gfxdraw.filled_circle(screen, right_x, right_y, JOY_CIRCLE_RADIUS // 2, (255, 255, 255))
