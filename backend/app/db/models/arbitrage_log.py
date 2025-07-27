# backend/app/db/models/arbitrage_log.py

from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.sql import func
from app.db.session import Base


class ArbitrageLog(Base):
    """
    Registro de ejecuciones o detecciones de arbitraje.
    Guarda los símbolos, precios, diferencia %, resultado, y estrategia usada.
    """

    __tablename__ = "arbitrage_log"

    id = Column(Integer, primary_key=True, index=True)
    strategy_name = Column(String, index=True)              # e.g. "SpotArbitrage"
    symbol_a = Column(String, index=True)                   # e.g. "BTCUSDT"
    symbol_b = Column(String, index=True)                   # e.g. "BTCBUSD"
    price_a = Column(Float)
    price_b = Column(Float)
    percent_diff = Column(Float)
    executed = Column(String, default="NO")                 # YES / NO / ERROR
    result = Column(JSON, nullable=True)                    # Info de órdenes si se ejecutó
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
