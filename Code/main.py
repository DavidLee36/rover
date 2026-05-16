import pygame
from enum import Enum

import controller
import config

class Screen(Enum):
	CONTROLLER = 0

current_screen = Screen.CONTROLLER

running = True
screen = None
clock = None
font = None

def init():
	global screen, clock, font
	pygame.init()
	controller.init()

	screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
	clock = pygame.time.Clock()
	font = pygame.font.SysFont("Arial", 18, bold=True)
	pygame.display.set_caption(config.TITLE)

def main_loop():
	while running:
		handle_input()
		draw()
		clock.tick(config.FPS)
	pygame.quit()

def handle_input():
	global running
	for event in pygame.event.get():
		if event.type == pygame.JOYDEVICEADDED:
			controller.on_device_added(event.device_index)
		if event.type == pygame.JOYDEVICEREMOVED:
			controller.on_device_removed(event.instance_id)
		if event.type == pygame.JOYAXISMOTION:
			controller.on_axis_motion(event.axis, event.value)
		if event.type == pygame.QUIT:
			running = False

def draw():
	screen.fill((0, 0, 0))
	if current_screen == Screen.CONTROLLER:
		controller.draw(screen)
	draw_fps()
	pygame.display.update()

def draw_fps():
	text = font.render(str(int(clock.get_fps())) + " fps", True, (255, 255, 255))
	screen.blit(text, (10, 10))

if __name__ == "__main__":
	init()
	main_loop()
