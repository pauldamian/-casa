'''
Created on Mar 20, 2016

@author: damianpa
'''
import datetime

def write(text):
    dt = datetime.datetime
    with open('acasa.log', 'a') as f:
        f.seek(0, 2)
        f.write(str(dt.now()) + ' ' + text + '\n')
