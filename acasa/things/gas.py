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


def alarm(pin):
    return gp.input(dig_pin)
