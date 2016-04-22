import sqlite3
from datetime import datetime
from acasa.CommandCenter.command import Command


conn = sqlite3.connect('laverda.db')
curs = conn.cursor()
curs.execute(' CREATE TABLE IF NOT EXISTS commands \
(cid INTEGER, message TEXT, data TEXT, schedule TEXT, commander TEXT)')


def insert_command(com):
    # query = "INSERT INTO commands VALUES({0},'{1}','{2}','{3}','{4}')".format(int(com.cid), com.order, com.data, com.schedule, com.commander)
    # print query
    c = (int(com.cid), com.order, str(com.data), str(com.schedule), com.commander)
    curs.execute("INSERT INTO commands VALUES(?, ?, ?, ?, ?)", c)


def read_current_commands():
    now = datetime.now()
    floor = now.replace(second=0, microsecond=0)
    if floor.minute == 59:
        ceil = floor.replace(hour=floor.hour + 1, minute=0)
    else:
        ceil = floor.replace(minute=floor.minute + 1)
    ttime = (str(floor), str(ceil))
    res = []
    for row in curs.execute("SELECT * FROM commands WHERE schedule\
     BETWEEN datetime(?) AND datetime(?)", ttime):
        c = Command(row[0], row[1], row[2], row[4])
        res.append(c)
    return res
