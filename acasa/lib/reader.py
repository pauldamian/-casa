from datetime import datetime as dt
from time import sleep

from things import constants as sc
from lib.todo import Todo
from lib import constants, util, command, log


class Reader(object):
    def __init__(self):
        self.db = Todo()
        self.users = util.get_conf_value(constants.KEY_USERS)
        self.things_dict = util.load_things_conf()
        self.things = self._load_things(self.things_dict)

    def _load_things(self, things_dict):
        things = []
        for thing_dict in things_dict:
            cls = thing_dict[sc.SENSOR_CLASS]
            module = thing_dict[sc.SENSOR_TYPE]
            thing = getattr(eval(module), cls)(
                thing_dict, thing_dict[sc.SENSOR_USE], location=thing_dict.get(sc.SENSOR_LOCATION),
                pin=thing_dict.get(sc.SENSOR_PIN, ""), tip=module,
                save_recordings=thing_dict.get(sc.SENSOR_SAVE_READS))

            things.append(thing)

        return things

    def alarm_all_users(self, alarm_message):
        for user in self.users:
            self.db.insert_command(command.Command(
                'SHOW ALARM', user, status='COMPLETED', result=alarm_message))

    def register_reading(self, kind, value, source):
        if value:
            # TODO implement threshold alarms mechanism
            return self.db.insert_reading(str(dt.now()), kind, value, source)
        else:
            log.warning("Invalid readings from {} sensor ".format(source))

    def instant_read(self, sensor_type, location):
        target_sensors = [sensor for sensor in self.get_things_by_key(sc.SENSOR_USE, sensor_type)
                          if sensor.location == location]
        if target_sensors:
            return target_sensors[0].read(sensor_type)
        else:
            return "No {} sensor for {}".format(sensor_type, location)

    def get_things_by_key(self, key, key_value):
        return [thing for thing in self.things if key_value in getattr(thing, key)]

    def run(self):
        log.info('Reader process started')
        timer = 0
        recoding_devices = self.get_things_by_key(sc.SENSOR_SAVE_READS, 1)
        alarm_devices = [device for device in self.things if hasattr(device, "alarm")]
        while True:
            if timer % sc.RECORDING_FREQUENCY == 0:
                timer = 0
                for device in recoding_devices:
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