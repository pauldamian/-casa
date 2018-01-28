import RPi.GPIO as gp
from time import sleep
from things.thing import Thing
from lib import log

"""
Pin Mapping:
Pin 4 - VCC 5V
Pin 6 - GND
Pin 7 - self.sync - PWM
Pin 11 - GATE - Digital
"""


class ACDimmer(Thing):
    def __init__(self, name, use, location, pin, type, save_recordings=False):
        Thing.__init__(self, name, use, location, pin, type, save_recordings)
        self.dimming = 100
        self.ac_load = pin.get("gate")
        self.sync = pin.get("sync")
        self.frequency = 50  # Hz
        gp.setwarnings(False)
        gp.setmode(gp.BOARD)
        gp.setup(self.ac_load, gp.OUT)
        gp.setup(self.sync, gp.IN, pull_up_down=gp.PUD_UP)
        gp.add_event_detect(self.sync, gp.RISING, callback=self._zero_cross_int)

    def _zero_cross_int(self, arg):
        idle_time = self.dimming * 0.0001
        if idle_time == 0:
            gp.output(self.ac_load, True)
            return
        elif idle_time == 0.01:
            gp.output(self.ac_load, False)
            return
        else:
            gp.output(self.ac_load, False)
            sleep(idle_time)
            gp.output(self.ac_load, True)
        sleep(0.00001)
        gp.output(self.ac_load, False)

    def set_dim_level(self, percent):
        self.dimming = 100 - percent
