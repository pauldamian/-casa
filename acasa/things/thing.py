'''
Created on Jun 27, 2016

@author: damianpa
'''


class Thing():
    def __init__(self, name, use, pin=0, location=None, tip='sensor', save_readings=False):
        self.location = location
        self.pin = pin
        self.name = name
        self.use = use
        self.tip = tip
        self.save_readings = save_readings
