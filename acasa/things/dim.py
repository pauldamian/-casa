import RPi.GPIO as gp
from time import sleep
from lib import util
import constants
 
"""
Pin Mapping:
Pin 4 - VCC 5V
Pin 6 - GND
 
Pin 7 - SYNC - PWM
Pin 11 - GATE - Digital
"""

gm = util.get_sensor_attribute_value(constants.DIMMER, constants.SENSOR_PIN)
dimming = 100
AC_LOAD = gm['gate']
SYNC = gm['sync']
gp.setwarnings(False)
 
 
def _zero_cross_int(arg):
    global dimming
    idle_time = dimming * 0.0001
    if idle_time == 0:
        gp.output(AC_LOAD, True)
        return
    elif idle_time == 0.01:
        gp.output(AC_LOAD, False)
        return
    else:
        gp.output(AC_LOAD, False)
        sleep(idle_time)
        gp.output(AC_LOAD, True)
    sleep(0.00001)
    gp.output(AC_LOAD, False)
 
 
def set_dim_level(percent):
    global dimming
    dimming = 100 - percent
 
FREQ = 50 # Hz
gp.setmode(gp.BOARD)
gp.setup(AC_LOAD, gp.OUT)
gp.setup(SYNC, gp.IN, pull_up_down=gp.PUD_UP)
gp.add_event_detect(SYNC, gp.RISING, callback=_zero_cross_int)
