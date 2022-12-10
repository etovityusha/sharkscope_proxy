from enum import Enum
from functools import lru_cache
from pydantic import BaseSettings


class LoggerLevelEnum(Enum):
    debug = "debug"
    info = "info"
    warning = "warning"


class Settings(BaseSettings):
    listen_host: str
    listen_port: int
    logger_level: LoggerLevelEnum
    pyproxy_base_url: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
