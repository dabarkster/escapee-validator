#!/usr/bin/python3

import os
import pyfirmata
import pygame
import random
import time
import paho.mqtt.client as paho
from subprocess import Popen

board = pyfirmata.Arduino('/dev/ttyACM0')

broker="192.168.56.220"
port=1883

photo_path = '/home/pi/Pictures/'
font_path  = "/home/pi/escapee-validator/Fonts/"
sound_path = "/home/pi/escapee-validator/Sounds/"

display_width = 1024
display_height = 1280
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

pygame.init()
print("pypy")
test_img = photo_path + "test.jpg"
img = pygame.image.load(test_img)
#screen = pygame.display.set_mode((0,0));
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)
screen = pygame.display.set_mode((640, 480), pygame.NOFRAME);
area_text = pygame.Rect(0,0,400,400)
textBox = screen.subsurface(area_text)
textBox.fill(white)


def text_objects(text, font):
    textSurface = font.render(text, True, red)
    return textSurface, textSurface.get_rect()

def message_display(text):
    term = font_path + 'saucer.ttf'
    #os.path.exists(term)
    largeText = pygame.font.Font(term, 115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((area_text.width/2),(area_text.height/2))
    status = screen.blit(TextSurf,TextRect.center)
    pygame.display.update()
    time.sleep(2)


def main():
	message_display("Pass...")


main()
quit()

pin13 = board.get_pin('d:5:o')



while True:
	time.sleep(5)
	print("on")

	pin13.write(1)

	time.sleep(5)
	print("off")
	pin13.write(0)