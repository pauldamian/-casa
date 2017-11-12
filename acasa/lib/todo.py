import sqlite3
from datetime import datetime
from time import sleep
from os import path

from lib.command import Command
from lib import util, constants


class Todo:
    curs = None
    conn = None
    READINGS_TABLE = "readings"
    COMMANDS_TABLE = "commands"

    def __init__(self):
        db_file = path.join(util.get_conf_value(constants.KEY_CONF_PATH), constants.DB_NAME)
        self.conn = sqlite3.connect(db_file)
        self.curs = self.conn.cursor()
        self._execute('CREATE TABLE IF NOT EXISTS {} \
        (cid INTEGER PRIMARY KEY, message TEXT, data TEXT, schedule TEXT, \
        commander TEXT, status TEXT, result TEXT);'.format(Todo.COMMANDS_TABLE))
        self._execute("CREATE TABLE IF NOT EXISTS {} (date STRING PRIMARY KEY, type TEXT,\
        value REAL, source TEXT);".format(Todo.READINGS_TABLE))

    def _execute(self, query):
        try:
            result = self.curs.execute(query)
        except sqlite3.OperationalError:
            sleep(3)
            self._execute(query)
        return result

    def _get_free_id(self):
        self._execute('SELECT cid FROM {} WHERE cid < 10000000 \
                            ORDER BY cid DESC LIMIT 1;'.format(Todo.COMMANDS_TABLE))
        try:
            sid = int(self.curs.fetchone()[0])
        except TypeError:
            sid = 0
            util.log("New deployment")
        return sid + 1

    def get_latest_id(self):
        self._execute('select max(cid) from {};'.format(Todo.COMMANDS_TABLE))
        try:
            lid = int(self.curs.fetchone()[0])
        except TypeError:
            lid = 0
            util.log("New deployment")
        return lid

    def insert_command(self, cmd):
        if not cmd.cid:
            cmd.cid = self._get_free_id()

        com_fields = (int(cmd.cid), cmd.message, str(cmd.data), str(cmd.schedule), cmd.user,
                      cmd.status, cmd.result)
        try:
            self._execute("INSERT INTO {} VALUES(?, ?, ?, ?, ?, ?, ?);".format(Todo.COMMANDS_TABLE),
                          com_fields)
            self.conn.commit()
            util.log('Command %s registered successfully' % cmd.message)
            return 0
        except sqlite3.IntegrityError as ie:
            util.log(ie.message)
            util.log('Command already in the database.')
        except sqlite3.OperationalError as oe:
            util.log(oe.message)
        return 1

    def to_command(self, row):
        message = row[1]
        if len(message.split()) > 1:
            order = message.split()[0]
            arg = message.split(' ', 1)[1]
        else:
            order = row[1]
            arg = ''
        status = row[5]
        if status == 'COMPLETED':
            schedule = None
        else:
            schedule = row[3]
        c = Command(cid=row[0], message=order, user=row[2], date=row[4], args=arg,
                    schedule=schedule, result=row[6])
        return c

    def cancel_command(self, text):
        try:
            if text == 'all':
                for cid in [cmd.cid for cmd in self.get_next_commands()]:
                    self.update_command(cid, "status", "CANCELLED")
            else:
                cid = [cmd.cid for cmd in self.get_next_commands() if cmd.message == text][0]
                self.update_command(cid, "status", "CANCELLED")
            return 0
        except sqlite3.OperationalError as oe:
            util.log(oe.message)
            return 1

    def get_current_commands(self):
        return self.get_filtered_commands("status='NEW' AND schedule<{}".format(datetime.now()))

    def get_next_commands(self, limit=3):
        return self.get_filtered_commands("status=NEW", limit, order_by="schedule")

    def get_completed_commands(self):
        return self.get_filtered_commands("status='COMPLETED'")

    def get_filtered_commands(self, condition, limit=None, order_by=None):
        res = []
        query = "SELECT * FROM {} WHERE {}".format(condition)
        if order_by:
            query = "{} ORDER BY {}".format(query, order_by)
        if limit:
            query = "{} LIMIT {}".format(query, limit)
        try:
            for row in self._execute(query + ";"):
                res.append(self.to_command(row))

        except sqlite3.OperationalError as oe:
            util.log(oe.message)

        return res

    def update_command(self, cid, column, value):
        q = (value, cid)
        try:
            self._execute('UPDATE {} SET {}=? WHERE cid=?'.format(Todo.COMMANDS_TABLE, column), q)
            self.conn.commit()
            util.log("Command {} {} was updated to {}" % (cid, column, value))
        except sqlite3.OperationalError as oe:
            util.log(oe.message)

    def delete_command(self, cid):
        try:
            self._execute("DELETE FROM {} WHERE cid=?;".format(Todo.COMMANDS_TABLE), (cid,))
            self.conn.commit()
            util.log("Command %s was deleted" % str(cid))
        except sqlite3.OperationalError as oe:
            util.log(oe.message)

    def insert_reading(self, *values):
        '''
        Inserts sensor reading in the database.
        Even though the format is flexible (variable number of arguments, for future migration to
        NoSQL db) use the following format for now:
        :param: date <string> used as primary key
        :param: type <string> property name: temperature, humidity, etc
        :param: value <real> the actual measurement value
        :param: source <string> where this measurement was taken
        '''
        try:
            self._execute('INSERT INTO {} VALUES (?, ?, ?, ?)'.format(Todo.READINGS_TABLE), values)
            self.conn.commit()
            return 0
        except sqlite3.IntegrityError:
            util.log('{} table primary key violation'.format(Todo.READINGS_TABLE))
        except sqlite3.OperationalError as oe:
            util.log(oe.message)
        return 1

    def get_reading(self, measured_property, source='kitchen'):
        now = datetime.now()
        now = now.replace(hour=now.hour - 1)

        self._execute('SELECT AVG(?) FROM {} WHERE source is ? AND date > ?\
        ORDER BY date DESC LIMIT 3;'.format(Todo.READINGS_TABLE), (source, str(now)))
        try:
            result = self.curs.fetchone()
        except TypeError as te:
            util.log(te.message)
            return "No sensor readings recorded!"
        if result is None:
            raise ValueError
        return result
