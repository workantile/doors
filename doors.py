#!/usr/bin/python

####################
#                  #
# Define GPIO Pins #
#                  #
####################

RED_LED     = 11
GREEN_LED   = 13
DOOR_STRIKE = 15

####################
#                  #
# Set up GPIO Pins #
#                  #
####################

import atexit
import RPi.GPIO as GPIO
import time

#python-pyserial package. Not sure we need this. Grabbed based on
#http://allenmlabs.blogspot.se/2013/01/raspberry-pi-parallax-rfid-reader.html
import serial

#Find the RFID as a USB device
#TODO: script should find it if not at USB0
RFID_SERIAL = serial.Serial('/dev/ttyUSB0', 2400, timeout=1)

GPIO.setmode(GPIO.BOARD)
atexit.register(GPIO.cleanup)

GPIO.setup(DOOR_STRIKE, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)

#Be explicit with what we want
#lowVoltage of 0 is ground
lowVoltage = 0
highVoltage = 1

#Pull Enable Pin Low to make it readable
GPIO.output(DOOR_STRIKE, lowVoltage)

#When door is open
def open_door():
    print("Door is open");
    GPIO.output(GREEN_LED, highVoltage)
    GPIO.output(RED_LED, lowVoltage)
    GPIO.output(DOOR_STRIKE, highVoltage)

#When door is closed and locked
def close_door():
    print("Door is closed");
    GPIO.output(DOOR_STRIKE, lowVoltage)
    GPIO.output(GREEN_LED, lowVoltage)
    GPIO.output(RED_LED, highVoltage)

#############################################
#                                           #
# Verify a key with openings.workantile.com #
#                                           #
#############################################

from urllib import request

# Anna's key
KEY="1F00D0B045"

# Which door controller are we?
CONTROLLER="deadbeef01"


# Blocks for 5 seconds before resetting the door
def verify_key(key):
    url = "http://openings.workantile.com/access/%s/%s" % (CONTROLLER, key)
    if request.urlopen(url).read().decode() == "OK":
        open_door()
        time.sleep(5)
    close_door()
    RFID_SERIAL.flushInput() # ignore errors, no data


import sys
#sys.exit(0)

while True:
    string = RFID_SERIAL.read(12)   
    if len(string) == 0:
            print("No tag read")
            continue
    else:
        string = string[1:11] #exclude start x0A and stop x0D bytes
        print(string)
        verify_key(KEY)
