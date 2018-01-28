from datetime import datetime as dt
from time import sleep

from things import constants as sc
from things import sensor, actuator
from lib.db_connector import DBConnector
from lib import constants, util, command, log

global sensors


class Reader(object):
    def __init__(self):
        self.db = DBConnector()
        self.users = util.get_conf_value(constants.KEY_USERS)
        self.things = util.get_things(type="sensor")
        global sensors
        sensors = self.things

    def alarm_all_users(self, alarm_message):
        for user in self.users:
            self.db.insert_command(command.Command(
                'SHOW ALARM', user, status='COMPLETED', result=alarm_message))

    def register_reading(self, kind, value, source):
        if value:
            # TODO implement threshold alarms mechanism
            return self.db.insert_reading(date=str(dt.now()), property=kind,
                                          value=value, source=source)
        else:
            log.warning("Invalid readings from {} sensor ".format(source))

    @staticmethod
    def instant_read(sensor_type, location):
        target_sensors = [sensor for sensor in Reader.get_things_by_key(sc.SENSOR_USE, sensor_type)
                          if sensor.location == location]
        if target_sensors:
            return target_sensors[0].read(sensor_type)
        else:
            return "No {} sensor for {}".format(sensor_type, location)

    @staticmethod
    def get_things_by_key(key, key_value):
        log.info("Global sensors: {}".format(sensors))
        return [thing for thing in sensors if key_value == getattr(thing, key) or
                (isinstance(getattr(thing, key), list) and key_value in getattr(thing, key))]

    def run(self):
        log.info('Reader process started')
        timer = 0
        recording_devices = self.get_things_by_key(sc.SENSOR_SAVE_READS, True)
        alarm_devices = [device for device in self.things if hasattr(device, "alarm")]
        while True:
            if timer % sc.RECORDING_FREQUENCY == 0:
                timer = 0
                for device in recording_devices:
                    for key in device.use:
                        measurement = device.read(key)
                        self.register_reading(key, measurement[key], device.location)
            for device in alarm_devices:
                alarm = device.alarm()
                if alarm:
                    self.alarm_all_users(alarm)
                device.read()
            sleep(60)
            timer += 1


if __name__ == "__main__":
    reader = Reader()
    reader.run()
