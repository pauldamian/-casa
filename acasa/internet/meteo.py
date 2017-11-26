'''
Created on 4 apr. 2016

@author: Paul
'''
import time

from lib import constants, util

APPID = util.get_conf_value(constants.KEY_OPENWEATHER)
KELVIN_TO_CELSIUS = 273.15


def seconds_to_time(seconds):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(seconds))


class Meteo():
    def __init__(self, vreme, sun=False):
        self.temp = float(vreme['main']['temp']) - KELVIN_TO_CELSIUS
        self.general = vreme['weather'][0]['description']
        self.time = seconds_to_time(vreme['dt'])
        if sun is True:
            self.sunset = seconds_to_time(vreme['sys']['sunset'])
            self.sunrise = seconds_to_time(vreme['sys']['sunrise'])
        else:
            try:
                self.rain = vreme['rain']['3h']
            except KeyError:
                self.rain = 'unknown'


def get_current_weather():
    request_now = "http://api.openweathermap.org/data/2.5/weather?id=681290&APPID=" + APPID
    rnow = util.get_response(request_now)
    now = Meteo(rnow, True)
    return now


def get_forecast(hours):
    request_next = "http://api.openweathermap.org/data/2.5/forecast?id=681290&APPID=" + APPID
    rnext = util.get_response(request_next)
    nextw = Meteo(rnext["list"][hours/3 - 1])
    return nextw
