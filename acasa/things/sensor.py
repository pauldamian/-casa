from time import sleep
from multiprocessing import Pool

import RPi.GPIO as gp

from lib import log
from things.thing import Thing
from things import constants


class MagneticSensor(Thing):
    def __init__(self, name, use, pin, location=None, type="sensor", save_recordings=False):
        Thing.__init__(self, name, use, pin, location, type, save_recordings)
        gp.setmode(gp.BOARD)
        gp.setup(self.pin, gp.IN, pull_up_down=gp.PUD_DOWN)
        gp.add_event_detect(self.pin, gp.RISING, callback=self._set_open)
        self.open = 0

    def alarm(self):
        if self.open:
            return "Break-in attempt at {}".format(self.location)

    def _set_open(self, pin):
        self.open = 1

    def read(self, property=constants.OPEN_KEY):
        self.open = gp.input(self.pin)
        return {property, self.open}


class DHT(Thing):

    def __init__(self, name, use, pin, location=None, type="sensor", save_recordings=False):
        Thing.__init__(self, name, use, pin, location, type, save_recordings)

    def read(self, property, steps=3):
        try:
            import Adafruit_DHT as dht
        except ImportError as ie:
            log.error(ie)
            raise EnvironmentError(
                "{} requires Adafruit_DHT to function!".format(self.__class__.__name__))
        # Returns the averaged property value: temperature or humidity
        value = 0.0
        for _ in range(steps):
            humidity, temperature = dht.read_retry(dht.DHT11, self.pin)
            if property == constants.TEMP_KEY and temperature:
                value += temperature
            elif property == constants.HUM_KEY and humidity:
                value += humidity

            sleep(1)

        return {property: value/steps}


class Gas(Thing):

    def __init__(self, name, use, pin, location=None, type="sensor", save_recordings=False):
        Thing.__init__(self, name, use, pin, location, type, save_recordings)
        gp.setmode(gp.BOARD)
        gp.setup(self.pin, gp.IN, pull_up_down=gp.PUD_DOWN)
        gp.add_event_detect(self.pin, gp.RISING, callback=self._set_smoke)
        self.smoke = 0

    def alarm(self):
        if self.smoke:
            return 'High levels of gas/smoke detected [{}]!'.format(self.location)

    def _set_smoke(self, pin):
        self.smoke = 1

    def read(self, property=constants.GAS_KEY):
        self.smoke = (gp.input(self.pin) + 1) % 2
        return {property: self.smoke}


class TISensorTag(Thing):

    def __init__(self, name, use, pin, location=None, type="sensor", save_recordings=False):
        Thing.__init__(self, name, use, location=location, type=type, save_recordings=save_recordings)
        self.mac = pin  # SensorTag MAC address
        self.connect()

    def connect(self):
        try:
            from bluepy import sensortag
            from bluepy.btle import BTLEException
            self.exception = BTLEException
        except ImportError as ie:
            log.error(ie)
            raise EnvironmentError("{} requires bluepy to function!".format(self.__class__.__name__))

        try:
            log.info('SENSORTAG: You might have to press the side button to connect.')
            self.tag = sensortag.SensorTag(self.mac)
            log.info('SENSORTAG Connected!')
            pool = Pool(1)
            pool.apply_async(self._always_on, [self.tag])
            log.info('AlwaysOn feature activated')

        except BTLEException as bte:
            log.error(bte.message)

    def _always_on(self):
        while True:
            self.tag.connect(self.mac)
            sleep(0.3)

    def read(self, property):
        value = 0.0
        index = 1
        sensor_name = property
        if property == constants.TEMP_KEY:
            index = 0
            sensor_name = "humidity"
        sensor = getattr(self.tag, sensor_name)
        try:
            sensor.enable()
            sleep(1)
            for _ in range(3):
                value += sensor.read()[index]
            sensor.disable()
        except self.exception as bte:
            log.info(bte.message)
            if 'disconnected' or 'connect()' in bte.message:
                if self.connect():
                    return self.read(property)

        return {property: value / 3}

    def on_exit(self):
        self.tag.disconnect()
