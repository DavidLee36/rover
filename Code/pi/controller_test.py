# TEMPORARY diagnostic — verifies the SDL GameController API on the Pi.
# Run:  python3 Code/pi/controller_test.py   (Ctrl-C to quit)
# Confirms: pygame/SDL version, that the controller module exists, that
# buttons map to stable names, and the real axis value range.
# Safe to delete once we've confirmed the mapping.

import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")  # no window needed; works over SSH

import pygame
from pygame._sdl2 import controller

pygame.init()
controller.init()
try:
	controller.set_eventstate(True)  # ensure controller events are emitted
except Exception:
	pass  # not present / not needed on this version

BUTTON_NAMES = {
	pygame.CONTROLLER_BUTTON_A: "A",
	pygame.CONTROLLER_BUTTON_B: "B",
	pygame.CONTROLLER_BUTTON_X: "X",
	pygame.CONTROLLER_BUTTON_Y: "Y",
	pygame.CONTROLLER_BUTTON_BACK: "BACK (Select)",
	pygame.CONTROLLER_BUTTON_GUIDE: "GUIDE (Xbox)",
	pygame.CONTROLLER_BUTTON_START: "START",
	pygame.CONTROLLER_BUTTON_LEFTSTICK: "LS (left stick click)",
	pygame.CONTROLLER_BUTTON_RIGHTSTICK: "RS (right stick click)",
	pygame.CONTROLLER_BUTTON_LEFTSHOULDER: "LB",
	pygame.CONTROLLER_BUTTON_RIGHTSHOULDER: "RB",
	pygame.CONTROLLER_BUTTON_DPAD_UP: "DPAD_UP",
	pygame.CONTROLLER_BUTTON_DPAD_DOWN: "DPAD_DOWN",
	pygame.CONTROLLER_BUTTON_DPAD_LEFT: "DPAD_LEFT",
	pygame.CONTROLLER_BUTTON_DPAD_RIGHT: "DPAD_RIGHT",
}
AXIS_NAMES = {
	pygame.CONTROLLER_AXIS_LEFTX: "LEFT_X",
	pygame.CONTROLLER_AXIS_LEFTY: "LEFT_Y",
	pygame.CONTROLLER_AXIS_RIGHTX: "RIGHT_X",
	pygame.CONTROLLER_AXIS_RIGHTY: "RIGHT_Y",
	pygame.CONTROLLER_AXIS_TRIGGERLEFT: "TRIGGER_L",
	pygame.CONTROLLER_AXIS_TRIGGERRIGHT: "TRIGGER_R",
}

print("pygame version:", pygame.version.ver)
print("SDL version:", pygame.version.SDL)
print("controllers detected:", controller.get_count())

controllers = {}
for i in range(controller.get_count()):  # open any already-connected pad
	if controller.is_controller(i):
		controllers[i] = controller.Controller(i)
		print(f"opened [{i}]: {controller.name_forindex(i)}")

print("\nPress each button / move sticks + triggers. Ctrl-C to quit.\n")

clock = pygame.time.Clock()
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.CONTROLLERDEVICEADDED:
			controllers[event.device_index] = controller.Controller(event.device_index)
			print("connected:", controller.name_forindex(event.device_index))
		elif event.type == pygame.CONTROLLERBUTTONDOWN:
			print("BTN DOWN:", BUTTON_NAMES.get(event.button, f"#{event.button}"))
		elif event.type == pygame.CONTROLLERBUTTONUP:
			print("BTN UP  :", BUTTON_NAMES.get(event.button, f"#{event.button}"))
		elif event.type == pygame.CONTROLLERAXISMOTION:
			if abs(event.value) > 8000:  # ignore idle jitter to cut spam
				print(f"AXIS {AXIS_NAMES.get(event.axis, event.axis)}: {event.value}")
	clock.tick(30)

pygame.quit()
