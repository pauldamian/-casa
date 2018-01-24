from pymongo import MongoClient
import json
from datetime import datetime
from lib.command import Command
# from lib import util, constants, log

class DBConnector(object):

    def __init__(self):
        self._client = MongoClient("192.168.100.8", 27017)
        self._db = self._client.acasa
        self._readings = self._db.sensor_data
        self._commands = self._db.commands

    ###############################################################################################
    # Operations on the commands collection
    ###############################################################################################
    @staticmethod
    def _decode_command(cmd_dict):
        return Command(cmd_id=cmd_dict.get("_id"),
                       message=cmd_dict.get("message"),
                       args=cmd_dict.get("args"),
                       date=cmd_dict.get("date"),
                       user=cmd_dict.get("user"),
                       schedule=cmd_dict.get("schedule"),
                       status=cmd_dict.get("status"),
                       result=cmd_dict.get("result"),
                       msg_id=cmd_dict.get("msg_id"))

    def get_greatest_property(self, name="_id", default=0):
        try:
            value = self._commands.find().sort([(name, -1)]).limit(1)[0].get(name)
        except IndexError:
            print("New deployment")
            value = default

        return value

    def insert_command(self, cmd):
        if not cmd.cmd_id:
            cmd.cmd_id = self.get_greatest_property() + 1

        self._commands.insert_one(cmd.to_json())

    def get_current_commands(self):
        return [self._decode_command(cmd) for cmd in self._commands.find(
            {"status": "NEW", "schedule": {"$lte": datetime.now()}})]

    def get_next_commands(self, limit=3):
        return [self._decode_command(cmd) for cmd in self._commands.find(
            {"status": "NEW"}).sort([("schedule", 1)]).limit(limit)]

    def get_completed_commands(self):
        return [self._decode_command(cmd)
                for cmd in self._commands.find({"status": "COMPLETED"})]

    def update_command(self, cmd_id, property, value):
        self._commands.update({"_id": cmd_id}, {"$set": {property: value}})

    def cancel_commands(self, pattern):
        if pattern == 'all':
            self._commands.update({"status": "NEW"}, {"$set": {"status": "CANCELLED"}})
        else:
            self._commands.update({"status": "NEW", "message": pattern},
                                  {"$set": {"status": "CANCELLED"}})

    def delete_command(self, cmd_id):
        self._commands.delete_one({"_id": cmd_id})

    ###############################################################################################
    # Operations on the sensor data collection
    ###############################################################################################

    def insert_reading(self, **values):
        self._readings.insert_one(values)

    def get_reading(self, property, source):
        now = datetime.now()
        now = now.replace(hour=now.hour - 1)
        data = list(self._readings.find({"property": property, "source": source,
                                         "date": {"$gte": now}}))
        return sum([read.get("value") for read in data])/len(data)

# db = client.admin
db = DBConnector()

# cmd = {
#     "_id": 102,
#     "name": "test",
#     "status": "NEW",
#     "schedule": datetime.now()
# }
# db._commands.insert_one(cmd)
# db.update_command(101, "status", "NEW")
# db.update_command(101, "user", "mue")
# db.update_command(100, "message", "show")
# db.insert_command(1)
# db.cancel_command("show")
# print(db.get_current_commands())
# print(list(db._commands.find()))

# db.insert_reading(value=18, source="home", property="temp", date=datetime.now())
# db.insert_reading(value=14, source="home", property="temp", date=datetime.now())
# db.insert_reading(value=51, source="home", property="hum", date=datetime.now())
#
# print(db.get_reading("temp", "home"))