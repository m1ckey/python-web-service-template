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
    jwt_key: bytes


@dataclass
class Config:
    env: Environment
    db: DBConfig
    gcp: GCPConfig
    server: ServerConfig
