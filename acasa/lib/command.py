from datetime import datetime
from lib import constants, util


class Command(object):

    def __init__(self, message, user, args="", schedule=None, date=None, status="NEW",
                 result="", cmd_id=None, msg_id=None):
        """

        :param message:
        :param user:
        :param args:
        :param schedule:
        :param date:
        :param status:
        :param result:
        :param cmd_id:
        :param msg_id:
        """
        self.cmd_id = cmd_id
        self.args = args
        self.message = message.lower()
        self.date = date or datetime.now()
        self.user = user
        self.schedule = schedule
        self.status = status
        self.result = result
        self.msg_id = msg_id

    def get_json(self):
        return {
            "_id": self.cmd_id,
            "message": self.message,
            "args": self.args,
            "date": self.date,
            "user": self.user,
            "schedule": self.schedule,
            "status": self.status,
            "result": self.result,
            "msg_id": self.msg_id
        }

    @staticmethod
    def get_valid_commands():
        return [constants.COMMAND_CANCEL,
                constants.COMMAND_SHOW,
                constants.COMMAND_LIGHTS
                ]

    @staticmethod
    def get_valid_date(date):
        if isinstance(date, datetime):
            return date
        elif isinstance(date, str):
            try:
                return datetime.strptime(date.split(".")[0], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                pass

        raise ValueError("Invalid schedule time. Please respect the given format.")

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, text):
        words = text.split()
        if len(words) > 1 and self.args is None:
            self.args = " ".join(words[1:])
        if words[0] in self.get_valid_commands():
            self._message = words[0]
        else:
            raise ValueError("Invalid command: {}!".format(text))

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, username):
        self._user = username
        # if username in util.get_conf_value(constants.KEY_USERS):
        #     self._user = username
        # else:
        #     raise ValueError("You are not authorized to perform this command.")

    @property
    def schedule(self):
        return self._schedule

    @schedule.setter
    def schedule(self, cmd_date):
        if not cmd_date:
            self._schedule = datetime.now()
        else:
            self._schedule = self.get_valid_date(cmd_date)
            # if self.schedule < datetime.now():
            #     raise ValueError("Invalid schedule time. Make sure that the date is in the future.")
