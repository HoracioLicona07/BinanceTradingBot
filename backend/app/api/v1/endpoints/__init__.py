# backend/app/api/v1/endpoints/__init__.py

from fastapi import APIRouter

from .health import router as health_router
from .prices import router as prices_router
from .strategies import router as strategies_router
from .arbitrage import router as arbitrage_router
from .trades import router as trade_router
from .performance import router as performance_router
from .dashboard import router as dashboard_router

api_router = APIRouter()

# Registrar todos los endpoints
api_router.include_router(health_router)
api_router.include_router(prices_router)
api_router.include_router(strategies_router)
api_router.include_router(arbitrage_router)
api_router.include_router(trade_router)
api_router.include_router(performance_router)
api_router.include_router(dashboard_router)
