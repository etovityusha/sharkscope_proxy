#!/usr/bin/env python
import subprocess
import sys

from environs import Env

from settings import get_settings

env = Env()
env.read_env()

if __name__ == "__main__":
    _component = sys.argv[1]
    match _component:
        case "web":
            _settings = get_settings()
            subprocess.call(
                " ".join(
                    [
                        "uvicorn",
                        "web:app",
                        "--reload",
                        "--port",
                        str(_settings.listen_port),
                        "--host",
                        _settings.listen_host,
                        "--log-level",
                        _settings.logger_level.value.lower(),
                    ]
                ),
                shell=True,
            )
        case _:
            raise Exception(f"Unknown component: {_component}")
