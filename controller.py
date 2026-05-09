import pygame
from pygame.locals import *

pygame.init()
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
clock = pygame.time.Clock()

# left x, left y, right x, right y
joy_motion = [0, 0, 0, 0]

def main():
    while True:
        handle_input()

def handle_input():
    for event in pygame.event.get():
        if event.type == JOYAXISMOTION:
            joy_motion[event.axis] = event.value
            sanatize_joy_input()
            print(joy_motion)

def sanatize_joy_input():
    for i in range(len(joy_motion)):
        if abs(joy_motion[i]) <= 0.15: # handle dead zone
            joy_motion[i] = 0
        if joy_motion[i] > 1: # clamp value from -1 to 1
            joy_motion[i] = 1
        if joy_motion[i] < -1:
            joy_motion[i] = -1
        joy_motion[i] = round(joy_motion[i], 2) # round to hundredths
main()