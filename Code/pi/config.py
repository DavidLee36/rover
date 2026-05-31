# REGION - CONSTANTS

# SCREEN
# SCREEN_WIDTH = 1024
# SCREEN_HEIGHT = 600
FPS = 100 # max
TITLE = "Rover"

# TEENSY
COM_WINDOWS = "COM4"
COM_LINUX = "/dev/ttyACM0"
BAUD = 115200

DEFAULT_SPEED = 50 # 0 - 100
MAX_SPEED = 100
MIN_SPEED = 0
SPEED_CHANGE = 0.15 # Rate at which to change curr_max_speed per frame

# CONTROLLER INPUTS
A_BTN = 0
B_BTN = 1
X_BTN = 2
Y_BTN = 3
LB_BUTTON = 4 # left bumper
RB_BTN = 5 # right bumper
SELECT_BTN = 6
START_BTN = 7
LS_BTN = 8 # left stick
RS_BTN = 9 # right stick
XBOX_BTN = 10



# REGION - MUTABLE

curr_max_speed = DEFAULT_SPEED