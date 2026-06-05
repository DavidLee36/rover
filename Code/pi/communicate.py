import serial

import config as config

ser = serial.Serial(config.COM_LINUX, config.BAUD, timeout=0.1)
ser.reset_input_buffer()

def close():
	ser.close()

def send(msg):
	ser.write((msg+"\n").encode())
	return ser.readline().decode('utf-8', errors='ignore').strip()

## Convert controller.axis_motion to string teensy expects
def axis_motion_to_teensy(arr):
	left_dir = "F" if arr[1] > 0 else "R"
	right_dir = "F" if arr[3] > 0 else "R"
	r_multi = config.curr_right_multiplier if left_dir and right_dir else 1
	return f"{left_dir}{round(abs(arr[1]) * config.curr_max_speed)}|{right_dir}{round(abs(arr[3]) * config.curr_max_speed * r_multi)}"