'''
Created on Mar 15, 2016

@author: damianpa
'''
# http://api.sunrise-sunset.org/json?lat=46.770439&lng=23.591423
# module that gets the sunset and sunrise times in order to automatically
# control the lightning [and curtains]
from datetime import datetime

#from CommandCenter import scheduler
from Utils import internet
# execfile("bla")

def add_hours(hour, delta):
    hour = hour.split(':')
    hour[0] = str(int(hour[0]) + delta)
    return ':'.join(hour)

# get sunrise and sunset times from internet location
request_url = "http://api.sunrise-sunset.org/json?lat=46.7693924&lng=23.590201&date="
now = str(datetime.now()).split()
r = internet.get_response(request_url + now[0])
n_time = r['results']['sunset'].split()[0]
d_time = r['results']['sunrise'].split()[0]
# Localize
n_time = add_hours(n_time, 15)
d_time = add_hours(d_time, 3)


