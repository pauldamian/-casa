'''
Created on Jun 18, 2016

@author: damianpa
'''
from os import system
MAC = 'BC:6A:29:AB:23:E4' # SensorTag MAC address

status = system('gatttool -b %s -I' % MAC)
