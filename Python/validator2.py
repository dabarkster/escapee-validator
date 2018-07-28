#!/usr/bin/python3

import os
import pyfirmata
import pygame
import random
import time
#import paho.mqtt.client as paho
import paho.mqtt.client as mqtt #import the client1

from subprocess import Popen
from omxplayer.player import OMXPlayer
from time import sleep


photo_path = '/home/pi/Pictures/'
music_path = "/home/pi/Music/"
font_path  = "/home/pi/escapee-validator/Fonts/"
sound_path = "/home/pi/escapee-validator/Sounds/"
video_path = "/home/pi/escapee-validator/Videos/"

######################## PYFirmata Initialize ########################
board          = pyfirmata.ArduinoMega('/dev/ttyACM0')
it = pyfirmata.util.Iterator(board)
it.start()
time.sleep(0.01)

pin_keyswitch  = board.get_pin('d:24:i')
pin_bigbutt    = board.get_pin('d:2:i')
pin_plas1      = board.get_pin('d:3:o')
pin_plas2      = board.get_pin('d:4:o')
pin_latch_butt = board.get_pin('d:5:i')
pin_latch      = board.get_pin('d:6:o')
pin_analyze    = board.get_pin('d:7:o')
#pin 8 is used for analyze LEDs
pin_lightning  = board.get_pin('d:9:o')
#pin 10 is use for lightning
pin_sending    = board.get_pin('d:11:o')
#pin 12 is used for sending
pin_uv         = board.get_pin('d:10:o')
#pin_fan always on
#pin_fog        = board.get_pin('d:12:o')
pin_arm        = board.get_pin('d:15:o')

pin = board.get_pin('d:13:o')


######################## PY Functions ########################

def text_objects(text, font):
    textSurface = font.render(text, True, red)
    return textSurface, textSurface.get_rect()

def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = pygame.font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while pygame.font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word      
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text

def message_display(text1, text2):
    #text1 = text[0]
    #text2 = text[1]

    print(text1)
    #textBox.fill(black)
    #textBox.set_alpha(50)
    #pygame.display.update()

    font = pygame.font.SysFont("Arial", 100)
    text_rect = (0,0)

    #pygame.display.flip()
    term = font_path + 'ready.otf'
    #os.path.exists(term)
    largeText = pygame.font.Font(term, 50)
    TextSurf, TextRect = text_objects("Power up", largeText)
    #TextRect.center = ((area_text.width/2),(area_text.height/2))
    textBox.blit(TextSurf, TextRect )
    
    #font = pygame.font.SysFont("Arial", 50)
    #text_surf = font.render("Pwer", True, (10,240,10))
    #textBox.blit(text_surf, text_rect)

    font = pygame.font.SysFont("Arial", 50)
    text_rect = (0,75)
    text_surf = font.render(text2, True, (240,240,240))
    textBox.blit(text_surf, text_rect)

    textBox.set_alpha(50)
    pygame.display.update()

######################## Other Functions ########################
def play_music(music_file):
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play()  #-1 = loop forever
    #pygame.mixer.music.set_volume(0.5)

def showvideo():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)
    movie = video_path + 'dna.mp4'
    player = OMXPlayer(movie)
    sleep(15)
    player.quit()
    #Popen(['omxplayer',  '--win', '"0 0 960 540"', movie])

def powerupanalyzer():
    message_display("Powering on validator...")
    play_music("power_up_analyzer.mp3")
    showvideo()
    #power up plasma1
    pin_plas1.write(1)

def analyze():
    global sample_failure
    global passed

    pin_analyzing.write(1)
    play_music("analyzing.mp3")
    if sample_failure == True:
        #run once
        message_display("Sample failure","Add more sample and re-test")
        sample_failure = False
        passed = False
    else:
        message_display("Sample success!","Sending sample to generator")
        time.sleep(3)
        pin_sending.write(1)
        time.sleep(3)
        passed = True
        

def powerupgenerator():
    message_display("Sending sample to generator....","Sending sample to generator")
    
    pin_lightning.write(1)
    play_sound("lightning.wav")
    time.sleep(5)
    pin.lightning.write(0)

    pin_fog.write(1)
    play_music("power_up_genrator.mp3")
    time.sleep(5)    
    pin_uv.write(1)
    time.sleep(5)
    message_display("Robotic arm ready to dispense cure....","Please extract")
    pin_arm.write(1)



######################## MQTT Functions ########################
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topicAll)

def on_message(client, userdata, msg):
    pass

def on_message_command(client, userdata, msg):
   
    msg.payload = msg.payload.decode("utf-8")

    if "override" in msg.payload:
        client.publish(topicStatus,"Overriding switch")
        powered_off = False

    if "open" in msg.payload:
        client.publish(topicStatus,"Opening door")
        pin_latch.write(1)

    if "analyze" in msg.payload:
        client.publish(topicStatus,"Analyze button pushed")
        pin_analyzing.write(1)

    if "generator" in msg.payload:
        client.publish(topicStatus,"Starting generator")
        powerupgenerator()

    if "arm" in msg.payload:
        client.publish(topicStatus,"Enabling arm...")
        pin_arm.write(1)

    if "lightning_on" in msg.payload:
        pin_lightning.write(1)


    if "lightning_off" in msg.payload:
        pin_lightning.write(0)

######################## PY Initialize ########################

pygame.init()
pygame.font.init()
print("Validator!")

screen_width = 1024
screen_height = 1280
photo_size = 400
photo_ratio = 536/820
photo_x = 200
photo_y = 200
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)



#screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN);

#### Dash ####
#dash_bottom = pygame.image.load(photo_path + '/validator_dash_bottom.png').convert()
#dash_bottom = pygame.transform.scale(dash_bottom, (screen_width, int(screen_height/2)))
#dash_top = pygame.image.load(photo_path + '/validator_dash_top.png').convert_alpha()
#dash_top = pygame.transform.scale(dash_top, (screen_width, int(screen_height/2)))
#dash_top = pygame.transform.rotate(dash_top, 180) 
#background_image = pygame.image.load(photo_path + '/validator_back.jpg').convert()
#background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

#area_photo = pygame.Rect(200,200,600,811)
#photo_box = screen.subsurface(area_photo)
#area_text = pygame.Rect(234, 758, 546, 288)
#mole_area = pygame.Rect(0,0,660,420)
#mole_box = screen.subsurface(mole_area)
#mole_box.fill(white)
#mole = pygame.image.load(photo_path + 'citric_acid.jpg').convert()
#mole = pygame.transform.scale(mole, (660,420))
#screen.blit(mole,[180,34])
#print(screen)
#print(area_text)
#screen.blit(dash_top, [0, 0])
#screen.blit(dash_bottom, [0, int(screen_height/2)])
#textBox = screen.subsurface(area_text)
#textBox.fill(white)


######drawText(textBox, "Chump", (0,0,250), area_text, "ready.otf", aa=False, bkg=None)
#pygame.display.flip()
#message_display("Power","Now")


######################## MQTT Initialize ########################
topic        = "escapee/validator"
topicAll     = topic + "/#"
topicStatus  = topic + "/status"
topicCommand = topic + "/command"
topicTimer   = topic + "/timer"

#broker="192.168.56.220"
broker_address="192.168.56.220" 
port=1883
client = mqtt.Client("client") 
client.on_connect = on_connect
client.message_callback_add(topicCommand, on_message_command)
client.on_message = on_message
client.connect(broker_address, 1883, 60) #connect to broker
client.loop_start()
client.publish(topicStatus,"Starting")#publish
time.sleep(1) #slight delay to show starting status
client.publish(topicStatus,"Waiting")


######################## Main ########################
def main():

    disable_latch = True
    powered_off = True
    passed = False
    sample_failure = True

    keyon = pin_keyswitch.read()
    while True: #not keyon:
        keyon = pin_keyswitch.read()
        print(keyon)
 

    #wait until key switch is turned on
    while powered_off == True:
        #while pin_keyswitch.read() == 0:
            powered_off = False
    
    print("up")
    quit()

    powerupanalyzer()
    disable_latch = False
    #open door
    pin_latch.write(1)

    while passed == False:
        while True:
            message_display("Press analyze button...")

            if pin_latch_butt.read() == 1:      
                client.publish(topicStatus,"Latch button pressed")
                if disable_latch == False:
                    pin_latch.write(1)
                else:
                    pin_latch.write(0)

            if pin_bigbutt.read() == 1:
                analyze()

    powerupgenerator()
    #message_display("Sending sample to generator....","Sending sample to generator")

    quit()

    gameexit = False
    while not gameexit:
        #pin_sending.write(1)
        pin_analyze.write(1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameexit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gameexit = True
                
    pygame.quit()
    quit()

if __name__ == "__main__":
    main()
