from datetime import datetime
from lib import constants, util

USERS = util.get_conf_value(constants.KEY_USERS)
valid_commands = [constants.COMMAND_CANCEL,
                  constants.COMMAND_SHOW,
                  constants.COMMAND_LIGHTS]


def valid_date(date):
    try:
        return datetime.strptime(date.split(".")[0], "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise ValueError("Invalid schedule time. Please respect the given format.")


class Command(object):

    def __init__(self, message, user, args="", schedule=None, date=None, status="NEW",
                 result="", c_id=None):
        self.cid = c_id
        self.message = message.lower()
        self.data = date or datetime.now()
        self.user = user
        self.args = args
        self.schedule = schedule
        self.status = status
        self.result = result

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, text):
        if text.split()[0] in valid_commands:
            self._message = text
        else:
            raise ValueError("Invalid command!")

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, username):
        if username in USERS:
            self._user = username
        else:
            raise ValueError("You are not authorized to perform this command.")

    @property
    def schedule(self):
        return self._schedule

    @schedule.setter
    def schedule(self, cmd_date):
        if not cmd_date:
            self._schedule = datetime.now()
        else:
            self._schedule = valid_date(cmd_date)
            if self.schedule < datetime.now():
                raise ValueError("Invalid schedule time. Make sure that the date is in the future.")
