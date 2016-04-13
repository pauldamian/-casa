import RPi.GPIO as gp
import time

"""
Pin Mapping:
Pin 4 - VCC 5V
Pin 6 - GND

Pin 7 - SYNC - PWM
Pin 11 - GATE - Digital
"""

AC_LOAD = 11
SYNC = 7
dimming = 3
FREQ = 50 # Hz


def zero_cross_int():
    global dimming
    dimtime = dimming * 0.0001
    time.sleep(dimtime)
    gp.output(AC_LOAD, True)
    time.sleep(0.00001)
    gp.output(AC_LOAD, False)

gp.setmode(gp.BOARD)
gp.setup(AC_LOAD, gp.OUT)
gp.setup(SYNC, gp.IN, pull_up_down=gp.PUD_UP)
gp.add_event_detect(SYNC, gp.RISING, callback=zero_cross_int)

while True:
    for i in range(10, 90, 5):
        dimming = i
        time.sleep(0.02)
    for i in range(90, 10, -5):
        dimming = i
        time.sleep(0.02)


def dim(level):
    dimming = level
