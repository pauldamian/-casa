'''
Created on 28 mar. 2016

@author: Paul
'''
# from datetime import datetime
from laverdadb import get_db_instance
import log
from twitter import notify
from time import sleep
from th import instant_th


def show_temp():
    temp, _  = instant_th()
    return 'Temperature is ' + str(temp) + '*C'

def show_hum():
    _, hum = instant_th()
    return 'Humidity is ' + str(hum) + '%'

def execute_command(command):
    log.write("Command %s will be executed now" % command.order)
##    c = command.order.replace(' ', '_')
    com = {'show temp' : show_temp,
           'show hum' : show_hum
           }
    res = com[command.order]()
    notify(res, command.commander)

def run():
    db = get_db_instance()
    while True:
        commands = db.read_current_commands()
        for command in commands:
            db.update_command_status(command.cid, 'IN PROGRESS')
            execute_command(command)
            db.update_command_status(command.cid, 'COMPLETED')
            log.write('command %s executed successfully' % command.order)
        sleep(5)
