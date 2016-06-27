'''
Created on 28 mar. 2016

@author: Paul
'''
from datetime import datetime
from keys import USERS

valid_commands = ['lights', 'show', 'cancel']


def valid_date(date):
    try:
        vdate = datetime.strptime(date.split('.')[0], '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return False
    return vdate


class Command:

    def __init__(self, cid, order, data, commander, status='NEW', args='', schedule=None, result=''):
        if order.lower().split()[0] not in valid_commands:
            self.cid = 0    # invalid command
            return
        if commander not in USERS:
            self.cid = -1   # unauthorized user
            return
        self.args = args
        if schedule is None:
            try:
                parts = order.split()[-2] + ' ' + order.split()[-1]
            except IndexError:
                self.cid = -3   # there's no command without arguments
                return
            if valid_date(parts) != False:
                self.schedule = valid_date(parts)
                order = ' '.join(order.split()[:-2])
            else:
                self.schedule = datetime.now()
        else:
            self.schedule = valid_date(schedule)
        if self.schedule is not False:
            # account for processing time
            if self.schedule < datetime.now().replace(minute=datetime.now().minute - 1):
                self.cid = -2
                return
        self.order = order.lower()
        self.cid = cid
        self.data = data
        self.commander = commander
        self.status = status
        self.result = result
