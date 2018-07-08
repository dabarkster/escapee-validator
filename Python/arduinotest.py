#!/usr/bin/python3

import pyfirmata
import time

board = pyfirmata.Arduino('/dev/ttyACM0')

pin13 = board.get_pin('d:5:o')

while True:
	time.sleep(5)
	print("on")

	pin13.write(1)

	time.sleep(5)
	print("off")
	pin13.write(0)