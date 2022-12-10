from functools import lru_cache

from pydantic import BaseSettings
from pymongo import MongoClient
from pymongo.database import Database


class MongoSettings(BaseSettings):
    mongo_username: str
    mongo_password: str
    mongo_host: str
    mongo_port: int
    mongo_database: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_mongo_settings():
    return MongoSettings()


@lru_cache()
def get_database() -> Database:
    settings = get_mongo_settings()
    client = MongoClient(
        f'mongodb://{settings.mongo_username}:{settings.mongo_password}'
        f'@{settings.mongo_host}:{settings.mongo_port}/'
    )
    return client[settings.mongo_database]
