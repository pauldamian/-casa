'''
Created on 16 iun. 2016

@author: Paul
'''
import RPi.GPIO as gp
import gpio_mapping as gm

dig_pin = gm.MQ2_DPIN

gp.setmode(gp.BOARD)
gp.setup(dig_pin, gp.IN, pull_up_down=gp.PUD_DOWN)
# gp.setup(dig_pin, gp.IN)
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
