from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.logger import logger
from app.api.v1.endpoints import (
    strategies,
    arbitrage,
    trades,
    performance,
    prices,
    dashboard,
    health,
)

app = FastAPI(
    title="Binance Trading Bot",
    version="1.0.0",
    description="🤖 Backend API para bot profesional de trading y arbitraje en Binance.",
)

# CORS settings (ajústalo para producción)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(strategies.router, prefix="/api/v1/strategies", tags=["Strategies"])
app.include_router(arbitrage.router, prefix="/api/v1/arbitrage", tags=["Arbitrage"])
app.include_router(trades.router, prefix="/api/v1/trades", tags=["Trades"])
app.include_router(performance.router, prefix="/api/v1/performance", tags=["Performance"])
app.include_router(prices.router, prefix="/api/v1/prices", tags=["Prices"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard"])
app.include_router(health.router, prefix="/api/v1", tags=["Health"])


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "🚀 BinanceTradingBot API is running"}


@app.on_event("startup")
async def startup_event():
    logger.info("🟢 FastAPI App Startup")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🔴 FastAPI App Shutdown")
