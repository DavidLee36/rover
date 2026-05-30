import pygame
from enum import Enum

import controller as controller
import communicate as comm
import config as config

class Screen(Enum):
	CONTROLLER = 0

current_screen = Screen.CONTROLLER

running = True
screen = None
clock = None
font = None
should_draw = True

update_teensy = False

def init():
	global screen, clock, font
	pygame.init()
	controller.init()

	screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
	clock = pygame.time.Clock()
	font = pygame.font.SysFont("Arial", 18, bold=True)
	pygame.display.set_caption(config.TITLE)

def main_loop():
	while running:
		handle_input()
		if should_draw: draw()
		if update_teensy:
			res = comm.send(comm.axis_motion_to_teensy(controller.axis_motion))
			#print(res)
		clock.tick(config.FPS)
	pygame.quit()

def handle_input():
	global running
	global update_teensy
	global should_draw
	update_teensy = False
	for event in pygame.event.get(): # Pygame events
		if event.type == pygame.JOYDEVICEADDED: # Controller connected
			controller.on_device_added(event.device_index)

		if event.type == pygame.JOYDEVICEREMOVED: # Controller disconnected
			controller.on_device_removed(event.instance_id)

		if event.type == pygame.JOYAXISMOTION: # Joystick or trigger movement
			controller.on_axis_motion(event.axis, event.value)
			update_teensy = True

		if event.type == pygame.QUIT: # Pygame window closed
			close()

		if event.type == pygame.JOYBUTTONUP:
			if event.button == config.RS_BTN: # Toggle drawing
				should_draw = not should_draw

	for joy in controller.joysticks: # Check controller input state vs pygame events
		if joy.get_button(config.SELECT_BTN) and joy.get_button(config.START_BTN): # Close keybind
			close()

		handle_speed_change(joy)

def handle_speed_change(joy):
	if joy.get_button(config.LB_BUTTON): # Reduce max speed
		config.curr_max_speed -= config.SPEED_CHANGE
		if config.curr_max_speed < config.MIN_SPEED: config.curr_max_speed = config.MIN_SPEED
	elif joy.get_button(config.RB_BTN): # Increase max speed
		config.curr_max_speed += config.SPEED_CHANGE
		if config.curr_max_speed > config.MAX_SPEED: config.curr_max_speed = config.MAX_SPEED
	config.curr_max_speed = round(config.curr_max_speed, 2)
	#print(config.curr_max_speed)

def draw():
	screen.fill((0, 0, 0))
	if current_screen == Screen.CONTROLLER:
		controller.draw(screen)
	draw_fps()
	pygame.display.update()

def draw_fps():
	text = font.render(str(int(clock.get_fps())) + " fps", True, (255, 255, 255))
	screen.blit(text, (10, 10))

def close():
	global running
	comm.close()
	running = False

if __name__ == "__main__":
	init()
	main_loop()
