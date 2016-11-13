'''
Created on 17 mai 2016

@author: Paul
'''

from datetime import datetime as dt
from time import sleep

from things import th
from things import gas
from things import constants as sc
from things.sensortag import TISensorTag
from utility.todo import Todo
from utility import constants, util

USERS = util.get_conf_value(constants.KEY_USERS)
db = Todo()

dth_dict = util.get_sensor_attribute_value(sc.DTH11)
dth = th.DHT(dth_dict[sc.SENSOR_TYPE], dth_dict[sc.SENSOR_USE],
             location=dth_dict[sc.SENSOR_LOCATION], pin=dth_dict[sc.SENSOR_PIN])

sensortag_dict = util.get_sensor_attribute_value(sc.SENSORTAG)
sensortag = TISensorTag(sensortag_dict[sc.SENSOR_TYPE], sensortag_dict[sc.SENSOR_USE],
                        location=sensortag_dict[sc.SENSOR_LOCATION], mac=sensortag_dict[sc.SENSOR_MAC])


def alarm_all_users(alarm_message):
    for user in USERS:
        cid = db.get_static_id()
        db.register_command(cid, 'SHOW ALARM', dt.now(), user, status='COMPLETED', result=alarm_message)


def register_reading(source, t, h, p):
    if (t, h, p) != (0, 0, 0):
        if t > sc.TEMPERATURE_THRESHOLD:
            alarm_all_users("{} temperature of {}*C registered!".format(t, source))
        if h > sc.HUMIDITY_THRESHOLD:
            alarm_all_users("{} humidity over {}%!".format(h, source))
        values = []
        values.append(str(dt.now()))
        values.append(t)
        values.append(h)
        values.append(p)
        values.append(source)
        return db.insert_reading(values)
    else:
        util.log("Invalid readings from {} sensor ".format(source))


def run():
    util.log('Reader process started')
    tag_connected = sensortag.init()
    minutar = 0
    while True:
        if minutar % sc.RECORDING_FREQUENCY == 0:
            minutar = 0
            t, h, p = dth.instant_th()
            register_reading(dth.location, t, h, p)
            if tag_connected:
                t, h, p = sensortag.get_all()
                register_reading(sensortag.location, t, h, p)
        if gas.alarm() == 1:
            alarm_all_users('High levels of gas/smoke detected!')
        gas.read()
        sleep(60)
        minutar += 1
