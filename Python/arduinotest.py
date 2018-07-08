#!/usr/bin/python3

import pyfirmata
import pygame
import random
import time
import paho.mqtt.client as paho
from subprocess import Popen

board = pyfirmata.Arduino('/dev/ttyACM0')

broker="192.168.56.220"
port=1883

photo_path = '/home/pi/Pictures'
font_path  = "/home/pi/escapee-validator/Fonts/"
sound_path = "/home/pi/escapee-validator/Sounds/"

display_width = 1024
display_height = 1280
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

pygame.init()
print("pypy")
img = pygame.image.load("test.jpg")
#screen = pygame.display.set_mode((0,0));
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)
screen = pygame.display.set_mode((640, 480), pygame.NOFRAME);






pin13 = board.get_pin('d:5:o')



while True:
	time.sleep(5)
	print("on")

	pin13.write(1)

	time.sleep(5)
	print("off")
	pin13.write(0)