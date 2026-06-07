# Controller button/axis names for the SDL GameController API.
#
# SDL normalizes every supported pad (Xbox, PS4, ...) onto this one semantic
# layout, so an Xbox "A" and a PS4 "Cross" both arrive as A_BTN. That means
# future PS4 support needs no new button ids here -- at most brand-specific
# display labels or action bindings, which can also live in this file.
#
# Imported elsewhere as `cmap` (short for controller map): cmap.A_BTN, etc.

import pygame

# BUTTONS
A_BTN = pygame.CONTROLLER_BUTTON_A
B_BTN = pygame.CONTROLLER_BUTTON_B
X_BTN = pygame.CONTROLLER_BUTTON_X
Y_BTN = pygame.CONTROLLER_BUTTON_Y
LB_BTN = pygame.CONTROLLER_BUTTON_LEFTSHOULDER   # left bumper
RB_BTN = pygame.CONTROLLER_BUTTON_RIGHTSHOULDER  # right bumper
SELECT_BTN = pygame.CONTROLLER_BUTTON_BACK
START_BTN = pygame.CONTROLLER_BUTTON_START
LS_BTN = pygame.CONTROLLER_BUTTON_LEFTSTICK       # left stick click
RS_BTN = pygame.CONTROLLER_BUTTON_RIGHTSTICK      # right stick click
GUIDE_BTN = pygame.CONTROLLER_BUTTON_GUIDE        # the Xbox/PS logo button
DPAD_UP = pygame.CONTROLLER_BUTTON_DPAD_UP
DPAD_DOWN = pygame.CONTROLLER_BUTTON_DPAD_DOWN
DPAD_LEFT = pygame.CONTROLLER_BUTTON_DPAD_LEFT
DPAD_RIGHT = pygame.CONTROLLER_BUTTON_DPAD_RIGHT

# AXES
LEFT_X = pygame.CONTROLLER_AXIS_LEFTX
LEFT_Y = pygame.CONTROLLER_AXIS_LEFTY
RIGHT_X = pygame.CONTROLLER_AXIS_RIGHTX
RIGHT_Y = pygame.CONTROLLER_AXIS_RIGHTY
TRIGGER_L = pygame.CONTROLLER_AXIS_TRIGGERLEFT
TRIGGER_R = pygame.CONTROLLER_AXIS_TRIGGERRIGHT

# SDL reports axes as ints in -32768..32767 (triggers 0..32767); divide by this
# to normalize sticks to ~-1..1 and triggers to 0..1.
AXIS_MAX = 32767.0
