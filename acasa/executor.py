'''
Created on 28 mar. 2016

@author: Paul
'''
# from datetime import datetime
from laverdadb import get_db_instance
import log
from twitter import notify
from time import sleep
from things import dim
from things.th import instant_th

db = get_db_instance()

# def show_temp(*args):
#     temp, _ = instant_th()
#     return 'Temperature is ' + str(temp) + '*C'


# def show_hum(*args):
#     pass
# 
# def lights_on(*args):
#     dim(0)
#     return 'Ok'
# 
# def lights_off(*args):
#     dim(99)
#     return 'Ok'
# 
# def dimm(*args):
#     level = args[0]
#     dim(level)
#     return 'Ok'

def show(arg):
    # Displays sensor readings
    if arg == 'temp':
        temp, _ = instant_th()
        return 'Temperature is ' + str(temp) + '*C'
    elif arg == 'hum':
        _, hum = instant_th()
        return 'Humidity is ' + str(hum) + '%'


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
        level = 0
    dim(level)
    return 'Ok'


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
