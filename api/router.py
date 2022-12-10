from fastapi.routing import APIRouter
from .stats.views import stats_router

api_router = APIRouter()
api_router.include_router(stats_router)
