from functools import lru_cache

import requests
from aiogram import Bot, Dispatcher, executor, types
from pydantic import BaseSettings


class TgBotSettings(BaseSettings):
    tg_bot_token: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_tg_bot_settings():
    return TgBotSettings()


bot = Bot(token=get_tg_bot_settings().tg_bot_token)


async def cmd_start(message: types.Message) -> None:
    await message.answer("Hello!")


async def all_other(message: types.Message) -> None:
    usernames = message.text.split(",")
    for username in usernames:
        response = requests.get(f"http://144.21.40.16:5000/stats/<str:username>?username={username}")
        if response.status_code == 200 and response.json()["found"]:
            await message.answer(f"{username}\n{response.json()['statistic']}")
        else:
            requests.post(f"http://144.21.40.16:5000/stats/new_or_refresh/<str:username>?username={username}")
    await message.answer("OK")


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_message_handler(cmd_start, commands='start')
    dispatcher.register_message_handler(all_other)


if __name__ == '__main__':
    dp = Dispatcher(bot)
    register_handlers(dp)
    executor.start_polling(dp, skip_updates=True)
