import json
import os
import sys
from base64 import b64decode

from dataclasses import dataclass
from enum import Enum, unique


@unique
class Environment(Enum):
    DEV = 0
    PROD = 1


@dataclass
class DBConfig:
    host: str
    port: int
    user: str
    password: str
    database: str


@dataclass
class GCPConfig:
    project_id: str


@dataclass
class ServerConfig:
    port: int
    jwt_key: bytes


class Config:
    env: Environment
    db: DBConfig
    gcp: GCPConfig
    server: ServerConfig

    @classmethod
    def load_config(cls):
        cls.env = Environment[os.environ.get('APP_ENV', Environment.DEV.name).upper()]
        print(f'env: {cls.env.name}', flush=True)

        path = f'config/config_{cls.env.name.lower()}.json'
        with open(path) as f:
            j = json.load(f)
            try:
                cls.db = DBConfig(
                    host=j['db']['host'],
                    port=j['db']['port'],
                    user=j['db']['user'],
                    password='',
                    database=j['db']['database']
                )
                cls.gcp = GCPConfig(
                    project_id=j['gcp']['project_id']
                )
                cls.server = ServerConfig(
                    port=j['server']['port'],
                    jwt_key=b''
                )
            except KeyError as e:
                print(f'could not parse {path}: {e}', file=sys.stderr)
                exit(1)

        if cls.env == Environment.PROD:
            from google.cloud import secretmanager
            client = secretmanager.SecretManagerServiceClient()

            name = f'projects/{cls.gcp.project_id}/secrets/db-password/versions/latest'
            cls.db.password = client.access_secret_version(name=name).payload.data.decode()
            name = f'projects/{cls.gcp.project_id}/secrets/server-jwt-key/versions/latest'
            cls.server.jwt_key = b64decode(client.access_secret_version(name=name).payload.data.decode())
        else:
            try:
                cls.db.password = os.environ['APP_DB_PASSWORD']
                cls.server.jwt_key = os.environ['APP_SERVER_JWT_KEY']
            except KeyError as e:
                print(f'could not parse environ: {e}', file=sys.stderr)
                exit(1)


Config.load_config()
