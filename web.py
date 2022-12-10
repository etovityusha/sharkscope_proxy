from fastapi import FastAPI

from api.router import api_router


def create_app() -> FastAPI:
    fastapi_app = FastAPI()
    fastapi_app.include_router(api_router)
    return fastapi_app


app = create_app()
