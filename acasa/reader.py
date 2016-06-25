'''
Created on 17 mai 2016

@author: Paul
'''
from todo import Todo
from datetime import datetime as dt
import log
from time import sleep
from things import th
from things import gas
from things import sensortag
from resources import USERS

db = Todo()


def register_reading(source, t, h, p):
    if (t, h, p) != (0, 0, 0):
        values = []
        values.append(str(dt.now()))
        values.append(t)
        values.append(h)
        values.append(p)
        values.append(source)
        db.insert_reading(values)
    else:
        log.write("Invalid readings from %s sensor " % source)


def run():
    gas_alarm_text = 'High levels of gas/smoke detected!'
    log.write('Reader process started')
    tag_connected = sensortag.init()
    minutar = 0
    while True:
        if minutar % 15 == 0:
            minutar = 0
#             t, h, p = th.instant_th()
#             register_reading(th.SOURCE, t, h, p)
            if tag_connected:
                t, h, p = sensortag.get_all()
                register_reading(sensortag.SOURCE, t, h, p)
        if gas.alarm() == 1:
            for user in USERS:
                cid = db.get_static_id()
                db.register_command(cid, 'SHOW SMOKE ALARM', dt.now(), user, status='COMPLETED',
                                    result=gas_alarm_text)
        gas.read()
        sleep(60)
        minutar += 1
