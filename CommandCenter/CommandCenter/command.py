'''
Created on 28 mar. 2016

@author: Paul
'''
import datetime
# commands mapping
commands = {}

class Command:
#    _command_schedule = {'Mon':[], 'Tue':[], 'Wed':[], 'Thu':[], 'Fri':[], 'Sat':[], 'Sun':[]}
    def __init__(self, schedule_time = None):
        if schedule_time is not None:
            self.timestamp = datetime.datetime.now()
        else:
            self.timestamp = schedule_time
            