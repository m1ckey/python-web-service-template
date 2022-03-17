import json
import os
import sys
from base64 import b64decode

from model import Config, Environment, DBConfig, GCPConfig, ServerConfig


def load_config() -> Config:
    env = Environment[os.environ.get('APP_ENV', Environment.DEV.name).upper()]
    print(f'env: {env.name}', flush=True)

    path = f'config/config_{env.name.lower()}.json'
    with open(path) as f:
        j = json.load(f)
        try:
            config = Config(
                env=env,
                db=DBConfig(
                    host=j['db']['host'],
                    port=j['db']['port'],
                    user=j['db']['user'],
                    password='',
                    database=j['db']['database']
                ),
                gcp=GCPConfig(
                    project_id=j['gcp']['project_id']
                ),
                server=ServerConfig(
                    jwt_key=b''
                )
            )
        except KeyError as e:
            print(f'could not parse {path}: {e}', file=sys.stderr)
            exit(1)

    if env == Environment.PROD:
        from google.cloud import secretmanager
        client = secretmanager.SecretManagerServiceClient()

        name = f'projects/{config.gcp.project_id}/secrets/db-password/versions/latest'
        config.db.password = client.access_secret_version(name=name).payload.data.decode("UTF-8")
        name = f'projects/{config.gcp.project_id}/secrets/server-jwt-key/versions/latest'
        config.server.jwt_key = b64decode(client.access_secret_version(name=name).payload.data.decode("UTF-8"))
    else:
        try:
            config.db.password = os.environ['APP_DB_PASSWORD']
            config.server.jwt_key = os.environ['APP_SERVER_JWT_KEY']
        except KeyError as e:
            print(f'could not parse environ: {e}', file=sys.stderr)
            exit(1)

    return config


config = load_config()
