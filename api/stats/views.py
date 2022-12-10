from pydantic import BaseModel

from db import get_database
from repo.stats import MongoStatsRepo
from services.sharkscope import Statistic
from worker import celery_app
from .router import stats_router


class StatsResponse(BaseModel):
    found: bool
    updated: str
    statistic: Statistic | None


@stats_router.get("/<str:username>", response_model=StatsResponse)
async def get_stats(username: str):
    repo = MongoStatsRepo(get_database())
    stats = repo.get_statistic(username)
    if stats is None:
        return StatsResponse(found=False, updated="", statistic=None)
    return StatsResponse(found=True, updated=stats.updated.isoformat(), statistic=Statistic.parse_obj(stats.dict()))


@stats_router.post("/new_or_refresh/<str:username>")
async def refresh_stats(username: str):
    celery_app.send_task("refresh_stats", args=[username])
    return {"message": "Refresh task sent"}


class Usernames(BaseModel):
    usernames: list[str]


@stats_router.post("/new_or_refresh")
async def refresh_stats(usernames: Usernames):
    for username in usernames.usernames:
        celery_app.send_task("refresh_stats", args=[username])
    return {"message": "Refresh task sent"}
