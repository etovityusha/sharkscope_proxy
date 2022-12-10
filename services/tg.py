import json
from functools import lru_cache

import requests
from pydantic import BaseSettings

from services.sharkscope import Statistic


class TgBotSettings(BaseSettings):
    tg_bot_token: str
    tg_chat_id: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_tg_bot_settings():
    return TgBotSettings()


def send_stats_to_tg(stats: Statistic, username: str) -> None:
    tg_bot_token = get_tg_bot_settings().tg_bot_token
    tg_chat_id = get_tg_bot_settings().tg_chat_id
    url = f"https://api.telegram.org/bot{tg_bot_token}/sendMessage"
    requests.post(url, data={"chat_id": tg_chat_id, "text": f"{username}\n{json.dumps(stats.dict(), indent=4)}"})
