from enum import Enum

import config as config

class ControlMode(Enum):
	DUAL_JOY = 0
	SINGLE_JOY = 1
	AUTONOMOUS = 2

curr_max_speed = config.DEFAULT_SPEED
curr_right_multiplier = config.DEFAULT_RIGHT_MULTIPLIER
curr_ctrl_mode = ControlMode.DUAL_JOY
