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
import threading
from multiprocessing import Pool

MAC = 'BC:6A:29:AB:23:E4' # SensorTag MAC address
SOURCE = 'outside'
tag = None


def always_on(tag):
    while True:
        tag.connect(MAC)
        sleep(0.3)


def init():
    global tag
    try:
        log.write('SENSORTAG: You might have to press the side button to connect.')
        tag = sensortag.SensorTag(MAC)
        log.write('SENSORTAG Connected!')
        pool = Pool(1)
        pool.apply_async(always_on, [tag])
#         ao = threading.Thread(target=always_on())
#         ao.daemon = True
#         ao.start()
        log.write('AlwaysOn feature activated')
        return True
    except BTLEException as bte:
        log.write(bte.message)
        return False


def get_humidity():
    global tag
    tag.humidity.enable()
    sleep(1)
    h = 0
    for i in range(3):
        h += tag.humidity.read()[1]
    tag.humidity.disable()
    return h / 3


def get_temperature():
    global tag
    tag.humidity.enable()
    sleep(1)
    t = 0
    for i in range(3):
        t += tag.humidity.read()[0]
    tag.humidity.disable()
    return t / 3


def get_pressure():
    global tag
    tag.barometer.enable()
    sleep(1)
    p = 0
    for i in range(3):
        p += tag.humidity.read()[1]
    tag.barometer.disable()
    return p / 3


def get_all():
    try:
        t = get_temperature()
        p = get_pressure()
        h = get_humidity()
        return t, h, p
    except BTLEException as bte:
        log.write(bte.message)
        if 'disconnected' or 'connect()' in bte.message:
            if init():
                get_all()
        return 0, 0, 0


def on_exit():
    tag.disconnect()
    del tag
