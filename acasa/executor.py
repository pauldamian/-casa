'''
Created on 28 mar. 2016

@author: Paul
'''
from todo import Todo
import log
from internet import meteo
from time import sleep
from help import help_text

from things import dim

db = Todo()
defaults = {'forecast': 3,
            'weather': 'city',
            'temp': 'inside',
            'hum': 'inside',
            'commands': 3
            }
sensor_location = {'temp': ['inside', 'outside'],
                   'hum': ['inside', 'outside'],
                   'pressure': ['outside'],
                   'weather': ['outside'],
                   'smoke': ['inside']
                   }


def show(arg):
    # Displays sensor readings
    what = arg.split()[0]
    try:
        where = arg.split()[1]
    except IndexError:
        where = defaults[what]
    result = ''
    if what == 'forecast':
        when = where
        return forecast(when)
    elif what == 'weather':
        if where == 'city':
            return forecast(0)
        else:
            if where not in sensor_location[what]:
                result += "No sensor in that location!\n"
            result += "Outside temperature is "
            try:
                temp, hum = db.get_reading(source=where)
            except (ValueError, TypeError):
                return "No records available"
            return result + str("%.1f" % temp) + '*C, while humidity reaches ' + str("%.1f" % hum) + '%'
    elif (what == 'temp') or (what == 'hum'):
        if where not in sensor_location[what]:
            return "No sensor in that location!"
        try:
            temp, hum = db.get_reading(source=where)
        except (ValueError, TypeError):
            return "No records available"
        if what == 'temp':
            return 'Temperature is ' + str("%.1f" % temp) + '*C'
        elif what == 'hum':
            return 'Humidity is ' + str("%.1f" % hum) + '%'
    elif what == 'commands':
        try:
            how_many = int(where)
        except ValueError:
            result = 'Invalid parameter for commands. Will return the next %s commands.\n' % defaults[what]
            how_many = defaults[what]
        coms = db.read_next_commands(how_many)
        if len(coms) == 0:
            result += "There are no commands scheduled"
        else:
            result += "The following commands will be executed:"
            for com in coms:
                result += "\n" + com.order + " " + com.args + " on " + str(com.schedule).split('.')[0]
        return result
    else:
        if (what in defaults):
            topic = what
        elif (where in defaults):
            topic = where
        try:
            return help_text['show'][topic]
        except KeyError:
            return help_text['help']


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
    return 'Lights turned ' + str(level)


def forecast(hours):
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
        h = 3
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
    if db.cancel_command(args) == 0:
        return 'Command canceled'
    else:
        return 'Error while canceling command'


def execute_command(command):
    log.write("Command %s will be executed now" % command.order)
    com = {'show': show,
           'lights': lights,
           'cancel': cancel
           }
    res = com[command.order](command.args)
    log.write(res)
    db.update_command_result(command.cid, res)
    return res
#    notify(res, command.commander)


def run():
    log.write('Executor process started')
    while True:
        commands = db.read_current_commands()
        for command in commands:
            db.update_command_status(command.cid, 'IN PROGRESS')
            res = execute_command(command)
            if res is not None:
                db.update_command_status(command.cid, 'COMPLETED')
            else:
                db.update_command_status(command.cid, 'FAILED')
            if command.order == 'cancel':
                break
            log.write('command %s executed successfully' % command.order)
        sleep(1)
