import logging
import sys

from config import ConfigProfile, conf


class Logger:
    def __init__(self):
        self.logger = logging.getLogger('main')
        self.logger.setLevel(logging.DEBUG)

        log_handler = logging.StreamHandler(sys.stdout)
        log_handler.setLevel(logging.ERROR if conf.profile == ConfigProfile.PROD else logging.DEBUG)
        log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)-8s - %(message)s'))
        self.logger.addHandler(log_handler)
