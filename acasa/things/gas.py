'''
Created on 16 iun. 2016

@author: Paul
'''
import RPi.GPIO as gp
import gpio_mapping as gm

dig_pin = gm.MQ2_DPIN
 
gp.setmode(gp.BOARD)
gp.setup(dig_pin, gp.IN, pull_up_down=gp.PUD_DOWN)
 
def alarm(pin):
    return 'Increased levels of smoke/gas detected!'
 
gp.add_event_detect(dig_pin, gp.RISING, callback=alarm)

