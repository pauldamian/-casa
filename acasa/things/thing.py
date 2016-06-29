'''
Created on Jun 27, 2016

@author: damianpa
'''


class Thing():
    def __init__(self, name, location=None, pin=0):
        self.location = location
        self.pin = pin
        self.name = name
