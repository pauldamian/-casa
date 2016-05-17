'''
Created on 28 mar. 2016

@author: Paul
'''
# from datetime import datetime
from laverdadb import Laverdadb
import log
from twitter import notify
from time import sleep
from __init__ import TEST

if not TEST:
    from things import dim
    from things.th import instant_th

db = Laverdadb()


def show(arg):
    # Displays sensor readings
    try:
        temp, hum = db.get_reading()
    except ValueError:
        return db.get_reading()
    if arg == 'temp':
        return 'Temperature is ' + str("%.1f" % temp) + '*C'
    elif arg == 'hum':
        return 'Humidity is ' + str("%.1f" % hum) + '%'


def lights(arg):
    # Controls the lights
    try:
        level = int(arg)
        if level > 100:
            level = 100
        elif level < 0:
            level = 0
    except ValueError:
        if arg == 'on':
            level = 100
        else:
            level = 0
    dim.set_dim_level(level)
    return 'Lights turned ' + arg


def cancel(args):
    db.cancel_command(args)
    return 'Command canceled'


def execute_command(command):
    log.write("Command %s will be executed now" % command.order)
#    c = command.order.replace(' ', '_')
    com = {'show': show,
           'lights': lights,
           'cancel': cancel
           }
    res = com[command.order](command.args)
    notify(res, command.commander)


def run():
    log.write('Executor process started')
    while True:
        commands = db.read_current_commands()
        for command in commands:
            db.update_command_status(command.cid, 'IN PROGRESS')
            execute_command(command)
            db.update_command_status(command.cid, 'COMPLETED')
            if command.order == 'cancel':
                break
            log.write('command %s executed successfully' % command.order)
        sleep(5)
