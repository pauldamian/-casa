'''
Created on 28 mar. 2016

@author: Paul
'''
from laverdadb import Laverdadb
import log
from internet import meteo
from time import sleep

from things import dim

db = Laverdadb()


def show(arg):
    # Displays sensor readings
    if arg.split()[0] == 'forecast':
        try:
            hours = arg.split()[1]
        except IndexError:
            hours = 0
        return _forecast(hours)
    try:
        temp, hum = db.get_reading()
    except ValueError:
        return db.get_reading()
    if arg == 'temp':
        return 'Temperature is ' + str("%.1f" % temp) + '*C'
    elif arg == 'hum':
        return 'Humidity is ' + str("%.1f" % hum) + '%'


def lights(intensity):
    # Controls the lights
    try:
        level = int(intensity)
        if level > 100:
            level = 100
        elif level < 0:
            level = 0
    except ValueError:
        if intensity == 'on':
            level = 100
        else:
            level = 0
    dim.set_dim_level(level)
    return 'Lights turned ' + intensity


def _forecast(hours):
    # returns weather forecast
    # hours refers to the prediction time
    # possible hours values: 0(now), 3, 6, 9
    try:
        h = int(hours)
        if h > 9:
            h = 9
        elif h < 0:
            h = 0
        elif h % 3 != 0:
            h = 3 * int((h + 1) / 3)
    except ValueError:
        h = 0
    if h == 0:
        w = meteo.get_current_weather()
        prefix = "The current weather condition is: "
    else:
        w = meteo.get_forecast(h)
        prefix = "The weather in %s hours will be " % h
    message = prefix + "%s with a temperature of %s*. " % (w.general, w.temp)
#    if h != 0:
#        message = message + "Chances of rain until then: %s" % w.rain
    return message


def cancel(args):
    db.cancel_command(args)
    return 'Command canceled'


def execute_command(command):
    log.write("Command %s will be executed now" % command.order)
    com = {'show': show,
           'lights': lights,
           'cancel': cancel
           }
    res = com[command.order](command.args)
    log.write(res)
    db.update_command_result(command.cid, res)
#    notify(res, command.commander)


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
        sleep(1)
