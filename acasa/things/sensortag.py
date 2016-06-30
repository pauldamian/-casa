'''
Created on Jun 18, 2016

@author: damianpa
'''
from os import system
from time import sleep
import pexpect
from bluepy import sensortag
from bluepy.btle import BTLEException
import log
from thing import Thing
import threading
from multiprocessing import Pool


class TISensorTag(Thing):
    tag = None

    def __init__(self, name, mac, location=None, pin=0):
        Thing.__init__(self, name, location)
        self.mac = mac # SensorTag MAC address

    def always_on(self, tag):
        while True:
            tag.connect(self.mac)
            sleep(0.3)

    def init(self):
        global tag
        try:
            log.write('SENSORTAG: You might have to press the side button to connect.')
            tag = sensortag.SensorTag(self.mac)
            log.write('SENSORTAG Connected!')
            pool = Pool(1)
            pool.apply_async(self.always_on, [tag])
    #         ao = threading.Thread(target=always_on())
    #         ao.daemon = True
    #         ao.start()
            log.write('AlwaysOn feature activated')
            return True
        except BTLEException as bte:
            log.write(bte.message)
            return False

    def get_humidity(self):
        global tag
        tag.humidity.enable()
        sleep(1)
        h = 0
        for i in range(3):
            h += tag.humidity.read()[1]
        tag.humidity.disable()
        return h / 3

    def get_temperature(self):
        global tag
        tag.humidity.enable()
        sleep(1)
        t = 0
        for i in range(3):
            t += tag.humidity.read()[0]
        tag.humidity.disable()
        return t / 3

    def get_pressure(self):
        global tag
        tag.barometer.enable()
        sleep(1)
        p = 0
        for i in range(3):
            p += tag.humidity.read()[1]
        tag.barometer.disable()
        return p / 3

    def get_all(self):
        try:
            t = self.get_temperature()
            p = self.get_pressure()
            h = self.get_humidity()
            return t, h, p
        except BTLEException as bte:
            log.write(bte.message)
            if 'disconnected' or 'connect()' in bte.message:
                if self.init():
                    self.get_all()
            return 0, 0, 0

    def on_exit(self):
        tag.disconnect()
        del tag
