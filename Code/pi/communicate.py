import serial

import config as config

ser = serial.Serial(config.COM, config.BAUD, timeout=0.1)

def send(msg):
	ser.write((msg+"\n").encode())
	return ser.readline().decode().strip()

## Convert controller.axis_motion to string teensy expects
def axis_motion_to_teensy(arr):
	left_dir = "F" if arr[1] > 0 else "R"
	right_dir = "F" if arr[3] > 0 else "R"
	return f"{left_dir}{abs(arr[1])*100}|{right_dir}{abs(arr[3]*100)}"