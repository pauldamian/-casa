'''
Created on 17 mai 2016

@author: Paul
'''
from laverdadb import Laverdadb
from datetime import datetime as dt
import log
from twitter import notify
from time import sleep
from things.th import instant_th

db = Laverdadb()

def run():
    while True:
        t, h = instant_th()
        values = []
        values.append(str(dt.now()))
        values.append(t)
        values.append(h)
        db.insert_reading(values)
        sleep(60)
