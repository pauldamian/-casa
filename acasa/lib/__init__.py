import logging as log
from os import path

from lib.util import get_conf_value, const

log_file = path.join(get_conf_value(const.KEY_LOG_PATH), get_conf_value(const.KEY_LOG_FILE))
log.basicConfig(level=log.DEBUG,
                format='%(asctime)s %(levelname)-7s: %(message)s',
                datefmt='%d-%m %H:%M:%S',
                filename=log_file
                )
