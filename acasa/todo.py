import sqlite3
from datetime import datetime
from time import sleep
from command import Command
import log


class Todo:
    curs = None
    conn = None

    def __init__(self):
        self.conn = sqlite3.connect('laverda.db')
        self.curs = self.conn.cursor()
        self.curs.execute('CREATE TABLE IF NOT EXISTS commands \
        (cid INTEGER PRIMARY KEY, message TEXT, data TEXT, schedule TEXT, commander TEXT, status TEXT, result TEXT);')
        self.curs.execute('CREATE TABLE IF NOT EXISTS thin (date STRING PRIMARY KEY, temp REAL, hum REAL);')

    def execute(self, query):
        try:
            result = self.curs.execute(query)
        except sqlite3.OperationalError:
            sleep(3)
            self.execute(query)
        return result

    def get_static_id(self):
        self.curs.execute('SELECT cid FROM commands WHERE cid < 10000000 \
                            ORDER BY cid DESC LIMIT 1;')
        try:
            sid = int(self.curs.fetchone()[0])
        except TypeError:
            sid = 0
            log.write("New deployment")
        return sid + 1

    def get_latest_id(self):
        self.curs.execute('select max(cid) from commands;')
        try:
            lid = int(self.curs.fetchone()[0])
        except TypeError:
            lid = 0
            log.write("New deployment")
        return lid

    def register_command(self, cid, message, data, commander, status='NEW', schedule=None, result=''):
        com = Command(cid, message, data, commander, status=status, schedule=schedule, result=result)
        if com.cid == 0:
            log.write('Invalid command')
        elif com.cid == -1:
            log.write('You are not authorized to perform this command.')
        if com.cid == -2:
            log.write('Invalid schedule time. Please respect the given format\
                and make sure that the date is in the future')
        else:
            return self.insert_command(com)
        return -1

    def insert_command(self, com):
        c = (int(com.cid), com.order, str(com.data), str(com.schedule), com.commander, com.status,
             com.result)
        try:
            self.curs.execute("INSERT INTO commands VALUES(?, ?, ?, ?, ?, ?, ?);", c)
            self.conn.commit()
            log.write('Command %s registered successfully' % com.order)
            return 0
        except sqlite3.IntegrityError:
            log.write('Command already in the database.')
        except sqlite3.OperationalError as oe:
            log.write(oe.message)
        return 1

    def to_command(self, row):
        message = row[1]
        if len(message.split()) > 1:
            order = message.split()[0]
            arg = message.split(' ', 1)[1]
        else:
            order = row[1]
            arg = ''
        c = Command(row[0], order, row[2], row[4], args=arg, schedule=row[3], result=row[6])
        return c

    def insert_reading(self, values):
        val = tuple(values)
        try:
            self.curs.execute('INSERT INTO thin VALUES (?, ?, ?)', val)
            self.conn.commit()
            return 0
        except sqlite3.IntegrityError:
            log.write('thin primary key violation')
        except sqlite3.OperationalError as oe:
            log.write(oe.message)
        return 1

    def get_reading(self):
        self.curs.execute('SELECT AVG(temp), AVG(hum) FROM thin ORDER BY date DESC LIMIT 3;')
        try:
            x = self.curs.fetchone()
            t, h = x
        except TypeError as te:
            log.write(te.message)
            return "No sensor readings recorded!"
        return t, h

    def cancel_command(self, text):
        if text == 'all':
            for cid in self.curs.execute("SELECT cid FROM commands WHERE status='NEW'").fetchall():
                self.update_command_status(cid[0], 'CANCELLED')
        else:
            cid = self.curs.execute("SELECT cid FROM commands WHERE message IS ? AND status='NEW' LIMIT 1", (text,)).fetchone()
            self.update_command_status(cid[0], 'CANCELLED')

    def read_current_commands(self):
        res = []
        now = str(datetime.now())
        try:
            for row in self.curs.execute("SELECT * FROM commands WHERE status='NEW' AND schedule<? ;",
                                         (now,)).fetchall():
                res.append(self.to_command(row))
        except sqlite3.OperationalError as oe:
            log.write(oe.message)
        return res

    def read_next_commands(self, number):
        res = []
        try:
            for row in self.curs.execute("SELECT * FROM commands WHERE status='NEW' ORDER BY schedule LIMIT ?;",
                                         (number,)).fetchall():
                res.append(self.to_command(row))
        except sqlite3.OperationalError as oe:
            log.write(oe.message)
        return res

    def get_completed_commands(self):
        res = []
        try:
            for row in self.curs.execute("SELECT * FROM commands WHERE status='COMPLETED';").fetchall():
                res.append(self.to_command(row))
        except sqlite3.OperationalError as oe:
            log.write(oe.message)
        return res

    def update_command_status(self, cid, status):
        q = (status, cid)
        try:
            self.curs.execute('UPDATE commands SET status=? WHERE cid=?', q)
            self.conn.commit()
            log.write("Command %s was marked as %s" % (cid, status))
        except sqlite3.OperationalError as oe:
            log.write(oe.message)

    def update_command_result(self, cid, result):
        q = (result, cid)
        try:
            self.curs.execute('UPDATE commands SET result=? WHERE cid=?', q)
            self.conn.commit()
            log.write("Command %s result was updated to %s" % (cid, result))
        except sqlite3.OperationalError as oe:
            log.write(oe.message)
