import logging
import sys

from config import conf
from model import Environment


class Logger:
    def __init__(self):
        self.logger = logging.getLogger('main')
        self.logger.setLevel(logging.DEBUG)

        log_handler = logging.StreamHandler(sys.stdout)
        log_handler.setLevel(logging.ERROR if conf.env == Environment.PROD else logging.DEBUG)
        log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)-8s - %(message)s'))
        self.logger.addHandler(log_handler)

        if conf.env == Environment.PROD:
            import google.cloud.logging
            client = google.cloud.logging.Client()
            client.get_default_handler()
            client.setup_logging()
