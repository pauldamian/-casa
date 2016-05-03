'''
Created on 28 mar. 2016

@author: Paul
'''
from datetime import datetime

_command_schedule = {'Mon': [], 'Tue': [], 'Wed': [], 'Thu': [], 'Fri': [], 'Sat': [], 'Sun': []}
_latest_command = None


def cancel(command):
    key = command.timestamp.ctime().split(' ')[0]
    if command in _command_schedule[key]:
        _command_schedule[key].remove(command)
        pass # to be replaced with logging message
    else:
        pass


def schedule(command):
    key = command.timestamp.ctime().split()[0]
    _command_schedule[key].append(command)
    _latest_command = command


def undo():
    if _latest_command is not None:
        cancel(_latest_command)
        _latest_command = None
    else:
        pass


cancel('destroy')
print _command_schedule
