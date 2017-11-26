import logging as log
from os import path

from util import get_conf_value, const

log_file = path.join(get_conf_value(const.KEY_LOG_PATH), get_conf_value(const.KEY_LOG_FILE))
log.basicConfig(format="%(asctime) %(levelname)s:%(message)s", level=log.DEBUG, filename=log_file)
