'''
Created on Mar 20, 2016

@author: damianpa
'''
import datetime
import json
import requests
from os import path

import constants as const
import things.constants as sc

# DO NOT EDIT THE LINE BELOW
# IF YOU MODIFY THE LINE BELOW OR THE NAME OF THE MODULE,
# THEN YOU SHOULD ALSO CHANGE THE INSTALLATION SCRIPT
CONFIGURATION_FILE_PATH = "/etc/acasa/acasa.conf"


def log(text):
    dt = datetime.datetime
    try:
        conf_file = path.join(get_conf_value(const.KEY_LOG_PATH),
                              get_conf_value(const.KEY_LOG_FILE))
        with open(conf_file, 'a') as f:
            f.seek(0, 2)
            f.write(str(dt.now()) + ' ' + text + '\n')
    except IOError:
        print text


def get_response(request_url):
    return requests.get(request_url).json()


def load_things_conf():
    things_conf = path.join(get_conf_value(const.KEY_CONF_PATH),
                            get_conf_value(const.KEY_CONF_THINGS))
    try:
        return json.load(open(things_conf))
    except:
        log("Problem loading {}".format(things_conf))
        return {}


def get_conf_value(key):
    config = json.load(open(CONFIGURATION_FILE_PATH))
    return config.get(key, None)


def get_help(key):
    help_text = json.load(open(const.KEY_HELP))
    return help_text.get(key, help_text)


def get_sensors_attribute(attribute):
    '''
    Returns all the unique attribute values of sensors defined in things.conf
    :param attribute: <string> sensor attribute (i.e. location)
    '''
    all_things = load_things_conf()
    attributes = []
    for sensor in all_things.values():
        try:
            attributes += sensor[attribute]
        except KeyError:
            attributes.append("undefined")

    unique_list = set(attributes)

    return list(unique_list)


def get_sensors_use_by_location(location=None):
    all_things = load_things_conf()

    if location:
        locations = list(location)
    else:
        locations = get_sensors_attribute(sc.SENSOR_LOCATION)
    result = {}
    for loc in locations:
        result.update({loc: [sensor[sc.SENSOR_USE] for sensor in all_things.values()
                             if loc in sensor[sc.SENSOR_LOCATION]]})
    return result


def get_sensors_location_by_use(use=None):
    all_things = load_things_conf()
    if use:
        uses = list(use)
    else:
        uses = get_sensors_attribute(sc.SENSOR_USE)
    result = {}
    for us in uses:
        result.update({us: [sensor[sc.SENSOR_LOCATION] for sensor in all_things.values()
                            if us in sensor[sc.SENSOR_USE]]})
    return result


def get_sensor_attribute_value(sensor, attribute=None):
    all_things = load_things_conf()
    try:
        if attribute:
            return all_things[sensor][attribute]
        else:
            return all_things[sensor]
    except KeyError:
        log("Sensor {} does not have a {} attribute".format(sensor, attribute))
