import logging
import sys

from config import config
from model import Environment

logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)

log_handler = logging.StreamHandler(sys.stdout)
log_handler.setLevel(logging.ERROR if config.env == Environment.PROD else logging.DEBUG)
log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)-8s - %(message)s'))
logger.addHandler(log_handler)

if config.env == Environment.PROD:
    import google.cloud.logging

    client = google.cloud.logging.Client()
    client.get_default_handler()
    client.setup_logging()
