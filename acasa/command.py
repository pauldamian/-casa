'''
Created on 28 mar. 2016

@author: Paul
'''
from datetime import datetime
from resources import USERS

valid_commands = ['lights', 'help', 'lock', 'unlock', 'show', 'cancel']


def valid_date(date):
    try:
        vdate = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return None
    return vdate


class Command:
    #    _command_schedule = {'Mon':[], 'Tue':[], 'Wed':[], 'Thu':[], 'Fri':[], 'Sat':[], 'Sun':[]}
    def __init__(self, cid, order, data, commander, status='NEW', args=None, schedule=None):
        if (order.lower().split()[0] not in valid_commands) or (order.lower().split()[0] == 'help'):
            self.cid = 0
            return
        if commander not in USERS:
            self.cid = -1
            return
        if args is None:
            self.args = ''
        else:
            self.args = args
        if schedule is None:
            self.schedule = datetime.now()
        else:
            self.schedule = valid_date(schedule)
            if self.schedule is None:
                if self.schedule < datetime.now():
                    self.cid = -2
                    return
        self.order = order.lower()
        self.cid = cid
        self.data = data
        self.commander = commander
        self.status = 'NEW'
