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
music_path = "/home/pi/Music/"
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
screen = pygame.display.set_mode((1024, 1024), pygame.NOFRAME)
photo_area = pygame.Rect(0,0,400,400)
text_area = pygame.Rect(0,0,800,400)
textBox = screen.subsurface(text_area)
textBox.fill(white)

def startup():
    #Phoebe - Initiating validator startup sequence...
    pass

def validating():
    #Phoebe - Validating formula...
    
    #fail
    #Phoebe - Insuffucuent quantity of antidote, please add 10mL more...
    
    #pass
    #Phoese - Formula for antidote is valid!  Sending antidotef ormula to generator....
    
    #start_generator()
    pass

def start_generator():
    #Phoebe - Sending formula to generator...
    pass

def generator():
    #Phobe - Antidote is complete, extract antidote from generator...
    pass

def text_objects(text, font):
    textSurface = font.render(text, True, red)
    return textSurface, textSurface.get_rect()

def message_display(text):
    screen.fill(pygame.Color("Black"), text_area)
    pygame.display.update()
    term = font_path + 'saucer.ttf'
    #os.path.exists(term)
    largeText = pygame.font.Font(term, 40)
    TextSurf, TextRect = text_objects(text, largeText)
    #TextRect.center = ((text_area.width/2),(text_area.height/2))
    #status = screen.blit(TextSurf,TextRect.center)
    status = screen.blit(TextSurf, TextRect)
    pygame.display.update()

def play_music(music_file):
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play(-1)  #-1 = loop forever
    #pygame.mixer.music.set_volume(0.5)

def main():

    #message_display("Place sample into validator...")
    #time.sleep(1)
    #message_display("Press start button...")
    #time.sleep(1)
    music_file = music_path + "analyze.mp3"
    play_music(music_file)
    while True:
        pass

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
