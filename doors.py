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

def lock_door():
    print("Door is locked");
    GPIO.output(DOOR_STRIKE, OFF)
    GPIO.output(RED_LED, ON)
    GPIO.output(GREEN_LED, OFF)
    GPIO.output(YELLOW_LED, OFF);
lock_door()

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




import time
import datetime
from urllib import request
#############################################
#                                           #
# Verify a key with openings.workantile.com #
#                                           #
#############################################
CACHED_KEYS = set()
NEED_PING   = []
THIS_MONTH  = datetime.date.today().month

def ping_server(key):
    print("Pinging server with key: %s (%s/%s)" % (key, SERVER, key))
    with request.urlopen("%s/%s" % (SERVER, key)) as f:
        if f.read().decode() == "OK":
            CACHED_KEYS.add(key)
            return True
        else:
            CACHED_KEYS.remove(key)
    return False

def clear_cache():
    global THIS_MONTH

    today = datetime.date.today()
    if today.month != THIS_MONTH:
        print("Clearing key cache")
        CACHED_KEYS.clear()
    THIS_MONTH = today.month

def verify_key(key):
    print("Verifying key: %s" % key)
    GPIO.output(YELLOW_LED, ON);
    clear_cache()
    if key in CACHED_KEYS:
        print("Using cached key")
        NEED_PING.append(key)
        return True
    return ping_server(key)

def ping_keys():
    if len(NEED_PING) > 0:
        ping_server(NEED_PING[0])
        NEED_PING.pop(0)


#python-pyserial package. Not sure we need this. Grabbed based on
#http://allenmlabs.blogspot.se/2013/01/raspberry-pi-parallax-rfid-reader.html
import serial
###################
#                 #
# Run RFID Reader #
#                 #
###################

RFID_SERIAL = serial.Serial(RFID_PATH, 2400, timeout=1)

def read_key():
    string = RFID_SERIAL.read(12)
    RFID_SERIAL.flushInput() # ignore errors, no data
    if len(string) > 0:
        key = string[1:11].decode() #exclude start x0A and stop x0D bytes
        if key.isalnum():
            return key;
    return None

def read_rfid():
    try:
        key = read_key()
        if key and verify_key(key):
            unlock_door()
            time.sleep(5) # block for 5 seconds before resetting door
        lock_door()
        ping_keys()
    except Exception as e:
        print(e)
        lock_door()
        blink_leds()



def loop():
    while True:
        read_rfid()

if __name__ == "__main__":
    loop()
