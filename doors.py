#!/usr/bin/python


import socket
##################
#                #
# Default values #
#                #
##################

CONTROLLER  = socket.gethostname()
SERVER      = "localhost"
RFID_PATH   = "/dev/ttyUSB0"
YELLOW_LED  = 7
GREEN_LED   = 11
RED_LED     = 13
DOOR_STRIKE = 15



import os
####################
#                  #
# Read doorrc file #
#                  #
####################

for conf in [ "/etc/doorsrc", "./doorsrc" ]:
    if os.path.exists(conf):
        with open(conf) as f:
            exec(compile(f.read(), "doorsrc", 'exec'))



import atexit
import RPi.GPIO as GPIO
####################
#                  #
# Set up GPIO Pins #
#                  #
####################

GPIO.setmode(GPIO.BOARD)
atexit.register(GPIO.cleanup)

GPIO.setup(DOOR_STRIKE, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(YELLOW_LED, GPIO.OUT)


OFF = GPIO.LOW
ON  = GPIO.HIGH


def unlock_door():
    print("Door is unlocked");
    GPIO.output(DOOR_STRIKE, ON)
    GPIO.output(RED_LED, OFF)
    GPIO.output(GREEN_LED, ON)
    GPIO.output(YELLOW_LED, OFF)

#When door is closed and locked
def lock_door():
    print("Door is locked");
    GPIO.output(DOOR_STRIKE, OFF)
    GPIO.output(RED_LED, ON)
    GPIO.output(GREEN_LED, OFF)
    GPIO.output(YELLOW_LED, OFF);

# Turn all LEDs on
def leds_on():
    GPIO.output(RED_LED, ON)
    GPIO.output(GREEN_LED, ON)
    GPIO.output(YELLOW_LED, ON)

# Turn all LEDs off
def leds_off():
    GPIO.output(RED_LED, OFF)
    GPIO.output(GREEN_LED, OFF)
    GPIO.output(YELLOW_LED, OFF)

def blink_leds():
    print("Blinking LEDs")
    for i in range(5):
        if (i % 2) == 0:
            leds_on()
        else:
            leds_off()
        time.sleep(1)
    lock_door()

lock_door()



import time
from urllib import request
#############################################
#                                           #
# Verify a key with openings.workantile.com #
#                                           #
#############################################

# Blocks for 5 seconds before resetting the door
def verify_key(key):
    GPIO.output(YELLOW_LED, ON);
    with request.urlopen(SERVER + ("/%s" % key)) as f:
        if f.read().decode() == "OK":
            unlock_door()
            time.sleep(5)
    lock_door()


#python-pyserial package. Not sure we need this. Grabbed based on
#http://allenmlabs.blogspot.se/2013/01/raspberry-pi-parallax-rfid-reader.html
import serial
###################
#                 #
# Run RFID Reader #
#                 #
###################

RFID_SERIAL = serial.Serial(RFID_PATH, 2400, timeout=1)

def _do_read_rfid():
    string = RFID_SERIAL.read(12)
    if len(string) == 0:
        print("No tag read")
    else:
        key = string[1:11].decode() #exclude start x0A and stop x0D bytes
        print(key)
        verify_key(key)
        RFID_SERIAL.flushInput() # ignore errors, no data

def read_rfid():
    try:
        _do_read_rfid()
    except Exception as e:
        print(e)
        lock_door()
        blink_leds()



def loop():
    while True:
        read_rfid()

if __name__ == "__main__":
    loop()
