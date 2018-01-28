import json
import requests
from os import path

from lib import log
import lib.constants as const
import things.constants as sc
# keep it here as it is required to load things classes
from things import sensor, actuator

# DO NOT EDIT THE LINE BELOW
# IF YOU MODIFY THE LINE BELOW OR THE NAME OF THE MODULE,
# THEN YOU SHOULD ALSO CHANGE THE INSTALLATION SCRIPT
CONFIGURATION_FILE_PATH = "/etc/acasa/acasa.conf"


def get_response(request_url):
    return requests.get(request_url).json()


def load_things_conf():
    things_conf = path.join(get_conf_value(const.KEY_CONF_PATH),
                            get_conf_value(const.KEY_CONF_THINGS))
    try:
        things_dict = json.load(open(things_conf))
        log.debug("Things defined in {}: {}".format(things_conf, things_dict))
        return things_dict
    except (IOError, ValueError):
        log.info("Problem loading {}".format(things_conf))
        return {}


def get_things(things_dict=None, **kwargs):
    """
    Return Thing objects from the things configuration json
    :param things_dict: The things configuration json. If not set, the default is used.
    :param kwargs: provide a way of filtering the desired things
    :return: list of Things
    """
    if things_dict is None:
        things_dict = load_things_conf()
    things = []
    for key, thing_dict in things_dict.items():
        # filter the object
        for k, v in kwargs.items():
            if v not in thing_dict.get(k):
                continue

        cls = thing_dict.get(sc.SENSOR_CLASS)
        module = thing_dict.get(sc.SENSOR_TYPE)
        try:
            thing = getattr(eval(module), cls)(
                key, thing_dict[sc.SENSOR_USE], location=thing_dict.get(sc.SENSOR_LOCATION),
                pin=thing_dict.get(sc.SENSOR_PIN, ""), type=module,
                save_recordings=thing_dict.get(sc.SENSOR_SAVE_READS, False))

            things.append(thing)
        except Exception as e:
            log.error("Unable to load {} because {}".format(key, e))

    return things


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
        log.warning("Sensor {} does not have a {} attribute".format(sensor, attribute))
