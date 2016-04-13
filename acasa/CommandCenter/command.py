'''
Created on 28 mar. 2016

@author: Paul
'''
import datetime
# commands mapping
commands = {'dim'}


class Command:
    #    _command_schedule = {'Mon':[], 'Tue':[], 'Wed':[], 'Thu':[], 'Fri':[], 'Sat':[], 'Sun':[]}
    def __init__(self, cid, order, data, commander, args=None):
        if args is None:
            self.schedule = datetime.datetime.now()
            self.args = ''
        else:
            self.schedule = schedule_time
        self.order = message.lower()
        self.cid = cid
        self.date = data
        self.commander = commander 
        return self
