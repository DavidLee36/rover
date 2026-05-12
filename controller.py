import pygame
import pygame.gfxdraw
from pygame.locals import *
import time

class Rover:
	def __init__(self):
		# Dimensions
		self.screen_width = 1200
		self.screen_height = 720
		self.third_width = int(self.screen_width/3)
		self.half_height = int(self.screen_height/2)
		self.joy_circle_radi = 100

		pygame.init()
		pygame.joystick.init()

		self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
		self.clock = pygame.time.Clock()

		self.joy_motion = [0, 0, 0, 0]  # left x, left y, right x, right y
		self.running = True

	def run(self):
		self.setup()
		while self.running:
			self.handle_input()
			self.draw()
			self.clock.tick(144)
		pygame.quit()

	def setup(self):
		self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
		self.clock = pygame.time.Clock()
		self.font = pygame.font.SysFont("Arial", 18, bold=True)
		pygame.display.set_caption("Rover")

	def handle_input(self):
		for event in pygame.event.get():
			if event.type == JOYAXISMOTION:
				self.joy_motion[event.axis] = event.value
				self.sanitize_joy_input()
				print(self.joy_motion)
			if event.type == pygame.QUIT:
				self.running = False

	def sanitize_joy_input(self):
		for i in range(len(self.joy_motion)):
			if abs(self.joy_motion[i]) <= 0.15:  # handle dead zone
				self.joy_motion[i] = 0
			self.joy_motion[i] = max(-1, min(1, self.joy_motion[i]))  # clamp -1..1
			self.joy_motion[i] = round(self.joy_motion[i], 2)  # round to hundredths

	def draw(self):
		self.screen.fill((0, 0, 0))
		self.draw_joy_circles()
		self.draw_fps()
		pygame.display.update()

	def draw_joy_circles(self):
		# Outer circles
		pygame.gfxdraw.circle(self.screen, self.third_width, self.half_height, self.joy_circle_radi, (255, 255, 255))
		pygame.gfxdraw.circle(self.screen, (self.third_width*2), self.half_height, self.joy_circle_radi, (255, 255, 255))

		# Inner circles
		div_val = 1.5
		left_x = int(self.third_width + round(self.joy_motion[0] * (self.joy_circle_radi/div_val)))
		left_y = int(self.half_height + round(self.joy_motion[1] * (self.joy_circle_radi/div_val)))
		right_x = int(self.third_width*2 + round(self.joy_motion[2] * (self.joy_circle_radi/div_val)))
		right_y = int(self.half_height + round(self.joy_motion[3] * (self.joy_circle_radi/div_val)))

		pygame.gfxdraw.filled_circle(self.screen, left_x, left_y, int(self.joy_circle_radi/2), (255, 255, 255))
		pygame.gfxdraw.filled_circle(self.screen, right_x, right_y, int(self.joy_circle_radi/2), (255, 255, 255))

	def draw_fps(self):
		fps = str(int(self.clock.get_fps()))
		text = self.font.render(fps + " fps", True, (255, 255, 255))
		self.screen.blit(text, (10, 10))

if __name__ == "__main__":
	Rover().run()
