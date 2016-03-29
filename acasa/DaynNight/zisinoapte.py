'''
Created on Mar 15, 2016

@author: damianpa
'''
# http://api.sunrise-sunset.org/json?lat=46.770439&lng=23.591423

import requests

# execfile("bla")

r = requests.get("http://api.sunrise-sunset.org/json?lat=46.770439&lng=23.59142&date=today")
ctime = r.json()['results']['civil_twilight_end']
print ctime
