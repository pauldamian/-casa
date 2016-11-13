'''
Created on 28 mar. 2016

@author: Paul
'''
from time import sleep

from utility.todo import Todo
from utility import util, constants
from internet import meteo
from things import dim

db = Todo()
defaults = {
    constants.ARG_FORECAST: 3,
    constants.ARG_WEATHER: 'city',
    constants.ARG_TEMPERATURE: 'kitchen',
    constants.ARG_HUMIDITY: 'kitchen',
    constants.ARG_COMMANDS: 3
    }

sensor_location = util.get_sensors_location_by_use()


def show(arg):
    # Displays sensor readings
    what = arg.split()[0]
    try:
        where = arg.split()[1]
    except IndexError:
        where = defaults[what]
    result = ''
    if what == constants.ARG_FORECAST:
        when = where
        return forecast(when)
    elif what == constants.ARG_WEATHER:
        if where == defaults[constants.ARG_WEATHER]:
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
    elif (what == constants.ARG_TEMPERATURE) or (what == constants.ARG_HUMIDITY):
        if where not in sensor_location[what]:
            return "No sensor in that location!"
        try:
            temp, hum = db.get_reading(source=where)
        except (ValueError, TypeError):
            return "No records available"
        if what == constants.ARG_TEMPERATURE:
            return 'Temperature is ' + str("%.1f" % temp) + '*C'
        elif what == constants.ARG_HUMIDITY:
            return 'Humidity is ' + str("%.1f" % hum) + '%'
    elif what == constants.ARG_COMMANDS:
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
                result += "\n{} {} on {}".format(com.order, com.args, str(com.schedule).split('.')[0])
        return result
    else:
        if (what in defaults):
            topic = what
        elif (where in defaults):
            topic = where
        try:
            return util.get_help([constants.COMMAND_SHOW][topic])
        except KeyError:
            return util.get_help([constants.COMMAND_HELP])


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
    return "Lights turned {}%.".format(level)


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
    return message


def cancel(args):
    if db.cancel_command(args) == 0:
        return 'Command canceled'
    else:
        return 'Error while canceling command'


def execute_command(command):
    util.log("Command {} will be executed now".format(command.order))
    com = {constants.COMMAND_SHOW: show,
           constants.COMMAND_LIGHTS: lights,
           constants.COMMAND_CANCEL: cancel
           }
    res = com[command.order](command.args)
    util.log(res)
    db.update_command_result(command.cid, res)
    return res


def run():
    util.log('Executor process started')
    while True:
        commands = db.read_current_commands()
        for command in commands:
            db.update_command_status(command.cid, constants.STATUS_IN_PROGRESS)
            res = execute_command(command)
            if res is not None:
                db.update_command_status(command.cid, constants.STATUS_COMPLETED)
            else:
                db.update_command_status(command.cid, constants.STATUS_FAILED)
            if command.order == constants.COMMAND_CANCEL:
                break
            util.log('Command {} executed successfully'.format(command.order))
        sleep(1)
