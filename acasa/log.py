'''
Created on Mar 20, 2016

@author: damianpa
'''
import datetime


def write(text):
    dt = datetime.datetime
    try:
        with open('/var/log/acasa/acasa.log', 'a') as f:
            f.seek(0, 2)
            f.write(str(dt.now()) + ' ' + text + '\n')
    except IOError:
        print text
