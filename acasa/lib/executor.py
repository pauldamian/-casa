from time import sleep

from lib.db_connector import DBConnector
from lib import util, log
from lib import constants
from lib import reader
from internet import meteo
from things import constants as tc


class Executor(object):

    defaults = {
        constants.ARG_FORECAST: 3,
        constants.ARG_WEATHER: "city",
        constants.ARG_TEMPERATURE: "kitchen",
        constants.ARG_HUMIDITY: "kitchen",
        constants.ARG_COMMANDS: 3
        }

    def __init__(self):
        self.db = DBConnector()
        self.actuators = util.get_things(type="actuator")

    def show(self, *args, **kwargs):
        # Displays sensor readings
        # Todo see what's broken here (args not passed as expected)
        what = args[0]
        log.info("What: {}".format(what))
        try:
            where = args[1]
        except IndexError:
            where = self.defaults.get(what, "")
        except TypeError:
            return "Don't know what to show!"

        if what == constants.ARG_FORECAST:
            when = where
            return self.forecast(when)

        elif what in [constants.ARG_TEMPERATURE, constants.ARG_HUMIDITY, constants.ARG_PRESSURE]:
            try:
                value = self.db.get_reading(what, source=where)
            except (ValueError, TypeError):
                return "No records available"
            return "%s %s is %.1f" % (where, what, value)

        elif what == constants.ARG_GAS:
            if reader.Reader.instant_read(what, where):
                return "Gas/smoke has been detected by the sensor!"
            else:
                return "No gas/smoke detected by the sensor."

        elif what == constants.ARG_WINDOW:
            return "This command is not implemented at the moment."

        elif what == constants.ARG_COMMANDS:
            result = ""
            try:
                how_many = int(where)
            except ValueError:
                result = "Invalid parameter for commands. Returning the next {} commands.\n".format(
                    self.defaults.get(what))
                how_many = self.defaults[what]
            cmds = self.db.get_next_commands(how_many)
            if len(cmds) == 0:
                result += "There are no commands scheduled"
            else:
                result += "The following commands will be executed:"
                for com in cmds:
                    result += "\n{} {} on {}".format(
                        com.order, com.args, str(com.schedule).split(".")[0])

            return result

        else:
            topic = "undefined topic"
            if what in self.defaults:
                topic = what
            elif where in self.defaults:
                topic = where
            try:
                return util.get_help([constants.COMMAND_SHOW][topic])
            except KeyError:
                return util.get_help([constants.COMMAND_HELP])

    def lights(self, intensity, location=None):
        # Controls the lights
        all_lights = [act for act in self.actuators if constants.COMMAND_LIGHTS in act.use]
        if location:
            loc_lights = [act for act in all_lights if location == act.location][0]
        else:
            loc_lights = all_lights[0]

        try:
            level = int(intensity)
            if level > 100:
                level = 100
            elif level < 0:
                level = 0
        except ValueError:
            if intensity == "on":
                level = 100
            else:
                level = 0
        loc_lights.set_dim_level(level)
        return "Lights turned {}%.".format(level)

    def forecast(self, hours):
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

    def cancel(self, args):
        if self.db.cancel_commands(args) == 0:
            return "Command canceled"
        else:
            return "Error while canceling command"

    def execute_command(self, command):
        log.info("Command {} will be executed now".format(command.message))
        com = {constants.COMMAND_SHOW: self.show,
               constants.COMMAND_LIGHTS: self.lights,
               constants.COMMAND_CANCEL: self.cancel
               }
        try:
            res = com[command.message](command.args.split())
        except KeyError:
            res = "Unknown command: {}".format(command.message)

        log.info(res)
        self.db.update_command(command.cmd_id, "result", res)

        return res

    def run(self):
        log.info("Executor process started")
        while True:
            commands = self.db.get_current_commands()
            for command in commands:
                self.db.update_command(command.cmd_id, "status", constants.STATUS_IN_PROGRESS)
                res = self.execute_command(command)
                if res is not None:
                    self.db.update_command(command.cmd_id, "status", constants.STATUS_COMPLETED)
                else:
                    self.db.update_command(command.cmd_id, "status", constants.STATUS_FAILED)
                if command.message == constants.COMMAND_CANCEL:
                    break
                log.info("Command {} executed successfully".format(command.message))

            sleep(1)


if __name__ == "__main__":
    executor = Executor()
    executor.run()
