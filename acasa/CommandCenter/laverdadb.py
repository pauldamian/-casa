import sqlite3


class laverdadb:
    def __init__(self):
        self.conn = sqlite3.connect('laverda.db')
        self.curs = self.conn.cursor()
        self.curs.execute(' CREATE TABLE IF NOT EXISTS commands (cid INTEGER, message TEXT, data TEXT, schedule TEXT, commander TEXT)')

    def insert_command(self, com):
        query = "INSERT INTO commands VALUES({0},'{1}','{2}','{3}','{4}')".format(int(com.cid), com.order, com.data, com.schedule, com.commander)
        # print query
        self.curs.execute(query)
