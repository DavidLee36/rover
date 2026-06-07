import serial

import config as config
import state as state

ser = serial.Serial(config.COM_LINUX, config.BAUD, timeout=0.1)
ser.reset_input_buffer()

def close():
	ser.close()

def send(msg):
	ser.write((msg+"\n").encode())
	return ser.readline().decode('utf-8', errors='ignore').strip()

## Convert controller.drivetrain ([left, right], +1 = forward) to string teensy expects
def drivetrain_to_teensy(arr):
	# Teensy/motor wiring has F and R physically swapped, so positive
	# (forward, after the Y-flip in controller) must send "R"
	left_dir = "R" if arr[0] > 0 else "F"
	right_dir = "R" if arr[1] > 0 else "F"
	r_multi = state.curr_right_multiplier if left_dir == "R" and right_dir == "R" else 1
	return f"{left_dir}{round(abs(arr[0]) * state.curr_max_speed)}|{right_dir}{round(abs(arr[1]) * state.curr_max_speed * r_multi)}"