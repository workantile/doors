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
RED_LED     = 11
GREEN_LED   = 13
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



import time
from urllib import request
#############################################
#                                           #
# Verify a key with openings.workantile.com #
#                                           #
#############################################

# Blocks for 5 seconds before resetting the door
def verify_key(key):
    GPIO.output(YELLOW_LED, highVoltage);
    with request.urlopen(SERVER + ("/%s" % key)) as f:
        if f.read().decode() == "OK":
            GPIO.output(YELLOW_LED, lowVoltage);
            open_door()
            time.sleep(5)
    GPIO.output(YELLOW_LED, lowVoltage);
    close_door()



#python-pyserial package. Not sure we need this. Grabbed based on
#http://allenmlabs.blogspot.se/2013/01/raspberry-pi-parallax-rfid-reader.html
import serial
###################
#                 #
# Run RFID Reader #
#                 #
###################

RFID_SERIAL = serial.Serial(RFID_PATH, 2400, timeout=1)

def read_rfid():
    string = RFID_SERIAL.read(12)
    if len(string) == 0:
        print("No tag read")
        #continue
    else:
        key = string[1:11].decode() #exclude start x0A and stop x0D bytes
        print(key)
        verify_key(key)
        RFID_SERIAL.flushInput() # ignore errors, no data


while True:
    try:
        read_rfid()
    except Exception(e):
        print(e)
