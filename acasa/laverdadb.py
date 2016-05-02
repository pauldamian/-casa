import sqlite3
from datetime import datetime
from command import Command
import log


class laverdadb:
    curs = None
    conn = None

    def __init__(self):
        self.conn = sqlite3.connect('laverda.db')
        self.curs = self.conn.cursor()
        self.curs.execute('CREATE TABLE IF NOT EXISTS commands \
        (cid INTEGER UNIQUE, message TEXT, data TEXT, schedule TEXT, commander TEXT, status TEXT);')

    def get_latest_id(self):
        self.curs.execute('select cid from commands where status is "COMPLETED" \
                            order by cid desc limit 1;')
        try:
            lid = int(self.curs.fetchone()[0])
        except TypeError:
            lid = 0
            log.write("New deployment")
        return lid

    def insert_command(self, com):
        c = (int(com.cid), com.order, str(com.data), str(com.schedule), com.commander, com.status)
        try:
            self.curs.execute("INSERT INTO commands VALUES(?, ?, ?, ?, ?, ?);", c)
            self.conn.commit()
        except sqlite3.IntegrityError:
            log.write('Command already in the database.')

    def read_current_commands(self):
        res = []
        for row in self.curs.execute("SELECT * FROM commands WHERE status='NEW'").fetchall():
            message = row[1]
            if len(message.split()) > 1:
                order = message.split()[0]
                arg = message.split()[1]
            else:
                order = row[1]
                arg = ''
            c = Command(row[0], order, row[2], row[4], args=arg)
            res.append(c)
        return res

    def update_command_status(self, cid, status):
        q = (status, cid)
        try:
            self.curs.execute('UPDATE commands SET status=? WHERE cid=?', q)
            self.conn.commit()
        except sqlite3.OperationalError:
            log.write("The command %s probably executed, but failed to update its status")

db_instance = laverdadb()


def get_db_instance():
    return db_instance
