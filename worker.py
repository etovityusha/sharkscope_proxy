from functools import lru_cache
from json import dumps

import requests
from celery import Celery
from pydantic import BaseSettings

from db import get_database
from repo.stats import MongoStatsRepo, StatisticEntity
from services.proxy import PyProxyService
from services.sharkscope import DefaultSharkScopeSvc
from settings import get_settings


class RedisSettings(BaseSettings):
    redis_host: str
    redis_port: int

    class Config:
        env_file = ".env"


@lru_cache()
def get_redis_settings():
    return RedisSettings()


class TaskException(Exception):
    pass


celery_app = Celery(__name__, broker="redis://redis:6379/0")


class TgBotSettings(BaseSettings):
    tg_bot_token: str
    tg_chat_id: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_tg_bot_settings():
    return TgBotSettings()


@celery_app.task(name="refresh_stats", autoretry_for=(TaskException,), retry_kwargs={'max_retries': 7, 'countdown': 5})
def refresh_stats(username: str, tg_callback: bool = True):
    try:
        stats = DefaultSharkScopeSvc(PyProxyService(get_settings().pyproxy_base_url)).get_statistic(username)
    except Exception as e:
        print(str(e)[:100])
        raise TaskException
    MongoStatsRepo(get_database()).set_statistic(username, StatisticEntity(**stats.dict()))
    if tg_callback:
        tg_bot_token = get_tg_bot_settings().tg_bot_token
        tg_chat_id = get_tg_bot_settings().tg_chat_id
        requests.get(
            f"https://api.telegram.org/{tg_bot_token}/"
            f"sendMessage?chat_id={tg_chat_id}&text={dumps(stats.dict(), indent=2)}"
        )
    return True
