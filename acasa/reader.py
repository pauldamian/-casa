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
from things.sensortag import TISensorTag
from things import THINGS
from keys import USERS

db = Todo()
dth = th.DHT(THINGS['dht_sensor']['name'], location=THINGS['dht_sensor']['location'],
             pin=THINGS['dht_sensor']['pin'])
sensortag = TISensorTag(THINGS['sensortag']['name'], location=THINGS['sensortag']['location'],
                        mac=THINGS['sensortag']['MAC'])

gas_alarm_text = 'High levels of gas/smoke detected!'
TEMPERATURE_THRESHOLD = 40
HUMIDITY_THRESHOLD = 90


def alarm_all_users(alarm_message):
    for user in USERS:
        cid = db.get_static_id()
        db.register_command(cid, 'SHOW ALARM', dt.now(), user, status='COMPLETED', result=alarm_message)


def register_reading(source, t, h, p):
    if (t, h, p) != (0, 0, 0):
        if t > TEMPERATURE_THRESHOLD:
            alarm_all_users("Temperature of %s*C registered %s" % (str(t), source))
        if h > HUMIDITY_THRESHOLD:
            alarm_all_users("Humidity over %s%% %s!" % (str(h), source))
        values = []
        values.append(str(dt.now()))
        values.append(t)
        values.append(h)
        values.append(p)
        values.append(source)
        return db.insert_reading(values)
    else:
        log.write("Invalid readings from %s sensor " % source)


def run():
    log.write('Reader process started')
    tag_connected = sensortag.init()
    minutar = 0
    while True:
        if minutar % 15 == 0:
            minutar = 0
            t, h, p = dth.instant_th()
            register_reading(dth.location, t, h, p)
            if tag_connected:
                t, h, p = sensortag.get_all()
                register_reading(sensortag.location, t, h, p)
        if gas.alarm() == 1:
            alarm_all_users(gas_alarm_text)
        gas.read()
        sleep(60)
        minutar += 1
