'''
Created on Jun 27, 2016

@author: damianpa
'''


class Thing():
    def __init__(self, name, use, location=None, pin=0, tip='sensor'):
        self.location = location
        self.pin = pin
        self.name = name
        self.use = use
        self.tip = tip
