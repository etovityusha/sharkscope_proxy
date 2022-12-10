from services.proxy import PyProxyService
from services.sharkscope import DefaultSharkScopeSvc, Statistic
from settings import get_settings
from .router import stats_router
from fastapi.exceptions import HTTPException

_stats = {}


@stats_router.get("/<str:username>", response_model=Statistic)
async def get_stats(username: str):
    try:
        return _stats[username]
    except KeyError:
        raise HTTPException(status_code=404, detail="Username not found")


@stats_router.get("/<str:username>/refresh")
async def refresh_stats(username: str):
    _stats[username] = DefaultSharkScopeSvc(PyProxyService(get_settings().pyproxy_default_url)).get_statistic(username)
