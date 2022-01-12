import logging
import os
import sys
from base64 import b64decode
from enum import Enum

import yaml


class ConfigProfile(Enum):
    DEV = 1
    PROD = 2


class Config:
    def __init__(self):
        self.profile = ConfigProfile[os.environ.get('APP_PROFILE', ConfigProfile.DEV.name).upper()]
        print(f'starting with profile: {self.profile.name}', flush=True)

        self.logger = logging.getLogger('main')
        self.logger.setLevel(logging.DEBUG)

        log_handler = logging.StreamHandler(sys.stdout)
        log_handler.setLevel(logging.ERROR if self.profile == ConfigProfile.PROD else logging.DEBUG)
        log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)-8s - %(message)s'))
        self.logger.addHandler(log_handler)

        if self.profile == ConfigProfile.PROD:
            self._load_yml('config/config_prod.yml')

            import google.cloud.logging
            client = google.cloud.logging.Client()
            client.get_default_handler()
            client.setup_logging()

            from google.cloud import secretmanager
            client = secretmanager.SecretManagerServiceClient()

            name = f'projects/{self.gcp_project_id}/secrets/db-backend-password/versions/1'
            self.db_password = client.access_secret_version(name=name).payload.data.decode("UTF-8")
            name = f'projects/{self.gcp_project_id}/secrets/server-jwt-key/versions/1'
            self.server_jwt_key = b64decode(client.access_secret_version(name=name).payload.data.decode("UTF-8"))
        else:
            self._load_yml('config/config_dev.yml')
            try:
                self.db_password = os.environ['APP_DB_PASSWORD']
                self.server_jwt_key = os.environ['APP_SERVER_JWT_KEY']
            except KeyError as e:
                self.logger.critical(f'could not parse environ: {e}')
                exit(1)

    def _load_yml(self, path: str):
        with open(path) as f:
            conf = yaml.safe_load(f)
            try:
                self.gcp_project_id = conf['gcp']['project_id']

                self.db_host = conf['db']['host']
                self.db_port = conf['db']['port']
                self.db_user = conf['db']['user']
                self.db_database = conf['db']['database']
            except KeyError as e:
                self.logger.critical(f'could not parse {path}: {e}')
                exit(1)
