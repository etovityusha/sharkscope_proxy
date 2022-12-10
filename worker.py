from functools import lru_cache

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


@celery_app.task(name="refresh_stats", autoretry_for=(TaskException,), retry_kwargs={'max_retries': 7, 'countdown': 5})
def refresh_stats(username: str):
    try:
        stats = DefaultSharkScopeSvc(PyProxyService(get_settings().pyproxy_base_url)).get_statistic(username)
    except Exception as e:
        print(str(e)[:100])
        raise TaskException
    MongoStatsRepo(get_database()).set_statistic(username, StatisticEntity(**stats.dict()))
    return True
