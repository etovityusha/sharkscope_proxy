#!/usr/bin/env python
import subprocess
import sys

from settings import get_settings

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
        case "worker":
            subprocess.call("celery -A worker.celery_app worker -l info", shell=True)
        case _:
            raise ValueError(f"Unknown component: {_component}")
