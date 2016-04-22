'''
Created on 28 mar. 2016

@author: Paul
'''
# from datetime import datetime
import laverdadb
from acasa.Utils import log
from time import sleep


def execute_command(command):
    log.write("Command %s will be executed now" % command.order)


while True:
    commands = laverdadb.read_current_commands()
    for command in commands:
        execute_command(command)
    sleep(59)
