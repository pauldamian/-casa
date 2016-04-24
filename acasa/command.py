'''
Created on 28 mar. 2016

@author: Paul
'''
from datetime import datetime
# commands mapping
valid_commands = ['dim', 'help', 'lock', 'unlock', 'show']


class Command:
    #    _command_schedule = {'Mon':[], 'Tue':[], 'Wed':[], 'Thu':[], 'Fri':[], 'Sat':[], 'Sun':[]}
    def __init__(self, cid, order, data, commander,status='NEW', args=None):
        if (order.lower().split()[0] not in valid_commands) or (order.lower().split()[0] == 'help'):
            self.cid = 0
            return
        if args is None:
            self.schedule = datetime.now()
            self.args = ''
        else:
            self.schedule = datetime.now()
        self.order = order.lower()
        self.cid = cid
        self.data = data
        self.commander = commander
        self.status = 'NEW'
