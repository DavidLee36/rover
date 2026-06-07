import pygame
from enum import Enum

import controller as controller
import communicate as comm
import config as config

class Screen(Enum):
	CONTROLLER = 0

class ControlMode(Enum):
	DUAL_JOY = 0
	SINGLE_JOY = 1
	AUTONOMOUS = 2

current_screen = Screen.CONTROLLER
curr_ctrl_mode = ControlMode.DUAL_JOY

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

	#screen = pygame.display.set_mode((1200, 720))
	screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
	clock = pygame.time.Clock()
	font = pygame.font.SysFont("Arial", 18, bold=True)
	pygame.display.set_caption(config.TITLE)

def main_loop():
	while running:
		handle_input()
		if should_draw: draw()
		if update_teensy:
			pass
			res = comm.send(comm.drivetrain_to_teensy(controller.drivetrain))
			#print(res)
		clock.tick(config.FPS)
	pygame.quit()

def handle_input():
	global running, update_teensy, should_draw, curr_ctrl_mode
	events = pygame.event.get()

	for event in events:
		if event.type == pygame.QUIT:
			close()

	result = controller.handle_input(events)
	if result["close"]: close()
	if result["toggle_draw"]: should_draw = not should_draw
	if result["toggle_ctrl_mode"]:
		if curr_ctrl_mode == ControlMode.DUAL_JOY:
			curr_ctrl_mode = ControlMode.SINGLE_JOY
		else:
			curr_ctrl_mode = ControlMode.DUAL_JOY
	update_teensy = result["needs_update"]

def draw():
	screen.fill((0, 0, 0))
	if current_screen == Screen.CONTROLLER:
		controller.draw(screen)
	draw_fps()
	draw_max_speed()
	pygame.display.update()

def draw_fps():
	text = font.render(str(int(clock.get_fps())) + " fps", True, (255, 255, 255))
	screen.blit(text, (10, 10))

def draw_max_speed():
	textMax = font.render("max speed: " + str(config.curr_max_speed), True, (255, 255, 255))
	textRight = font.render("right multi: " + str(round(config.curr_right_multiplier, 2)), True, (255, 255, 255))
	screen.blit(textMax, (10, 30))
	screen.blit(textRight, (10, 50))

def close():
	global running
	comm.close()
	running = False

if __name__ == "__main__":
	init()
	main_loop()
