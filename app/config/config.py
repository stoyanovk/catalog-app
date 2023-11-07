import os
from dataclasses import dataclass

CONFIG = None


@dataclass
class Config:
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: str
    REFRESH_JWT_SECRET: str
    ACCESS_JWT_SECRET: str


def get_config():
    global CONFIG
    if not CONFIG:
        CONFIG = Config(
            POSTGRES_HOST=os.environ.get("POSTGRES_HOST", "127.0.0.1"),
            POSTGRES_USER=os.environ.get("POSTGRES_USER", "postgres"),
            POSTGRES_DB=os.environ.get("POSTGRES_DB", "catalog"),
            POSTGRES_PASSWORD=os.environ.get("POSTGRES_PASSWORD", "12345678"),
            POSTGRES_PORT=os.environ.get("POSTGRES_PORT", "5432"),
            ACCESS_JWT_SECRET=os.environ.get("ACCESS_JWT_SECRET", "access_secret"),
            REFRESH_JWT_SECRET=os.environ.get("ACCESS_JWT_SECRET", "refresh_secret"),
        )
    return CONFIG


__all__ = ["get_config"]
