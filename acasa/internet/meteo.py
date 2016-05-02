'''
Created on 4 apr. 2016

@author: Paul
'''
import internet
from acasa.resources import APPID
import time

KELVIN_TO_CELSIUS = 273.15


def seconds_to_time(seconds):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(seconds))


class Meteo():
    def __init__(self, vreme):
        self.temp = float(vreme['main']['temp']) - KELVIN_TO_CELSIUS
        self.general = vreme['weather'][0]['description']
        self.time = seconds_to_time(vreme['dt'])


request_next = "http://api.openweathermap.org/data/2.5/forecast?id=681290&APPID=" + APPID
request_now = "http://api.openweathermap.org/data/2.5/weather?id=681290&APPID=" + APPID
rnext = internet.get_response(request_next)
rnow = internet.get_response(request_now)

next3 = Meteo(rnext["list"][1])
next6 = Meteo(rnext['list'][2])
next9 = Meteo(rnext['list'][3])
now = Meteo(rnow)


# print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(rnow['sys']['sunset'])))
# print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(rnow['sys']['sunrise'])))
