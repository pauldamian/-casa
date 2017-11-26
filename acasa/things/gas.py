'''
Created on 16 iun. 2016

@author: Paul
'''
import RPi.GPIO as gp
from lib import util
import constants

dig_pin = util.get_sensor_attribute_value(constants.MQ2, constants.SENSOR_PIN)

gp.setmode(gp.BOARD)
gp.setup(dig_pin, gp.IN, pull_up_down=gp.PUD_DOWN)

SMOKE = 0

def _set_smoke(pin):
    global SMOKE
    SMOKE = 1

def alarm():
    return SMOKE

def read():
    global SMOKE
    SMOKE = (gp.input(dig_pin) + 1) % 2

gp.add_event_detect(dig_pin, gp.RISING, callback=_set_smoke)
