import sqlite3

class laverdadb:
    conn = sqlite3.connect('laverda.db')
    curs = conn.cursor()

    def __init__(self):
        return self.curs

    def insert_command(self, com):
        self.curs.execute("INSERT INTO commands VALUES({0},{1},{2},{3})".format(int(com.cid), com.order, com.data, com.commander))
