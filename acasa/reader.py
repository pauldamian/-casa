'''
Created on 17 mai 2016

@author: Paul
'''
from todo import Todo
from datetime import datetime as dt
import log
from time import sleep
from things.th import instant_th
from things import gas
import RPi.GPIO as gp
from resources import USERS

db = Todo()


def run():
    text = 'High levels of gas/smoke detected!'
    log.write('Reader process started')
    while True:
        t, h = instant_th()
        values = []
        values.append(str(dt.now()))
        values.append(t)
        values.append(h)
        db.insert_reading()
        if gas.alarm(1) == 0:
            for user in USERS:
                cid = db.get_static_id()
                db.register_command(cid, 'SHOW SMOKE ALARM', dt.now(), user, status='COMPLETED', result=text)

        sleep(60)
