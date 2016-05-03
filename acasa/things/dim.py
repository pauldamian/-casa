try:
    import RPi.GPIO as gp
except ImportError:
    print "Running compatibility mode"
from time import sleep

"""
Pin Mapping:
Pin 4 - VCC 5V
Pin 6 - GND

Pin 7 - SYNC - PWM
Pin 11 - GATE - Digital
"""

AC_LOAD = 11
SYNC = 7
dimming = 100
FREQ = 50 # Hz


def zero_cross_int(arg):
    global dimming
    dimtime = dimming * 0.0001
    sleep(dimtime)
    gp.output(AC_LOAD, True)
    sleep(0.00001)
    gp.output(AC_LOAD, False)


def start():
    global dimming
    global level
    gp.setmode(gp.BOARD)
    gp.setup(AC_LOAD, gp.OUT)
    gp.setup(SYNC, gp.IN, pull_up_down=gp.PUD_UP)
    gp.add_event_detect(SYNC, gp.RISING, callback=zero_cross_int)


def dim(percent):
    dimming = percent
