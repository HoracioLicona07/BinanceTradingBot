# backend/app/models/trade.py

from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.sql import func
from app.db.session import Base


class Trade(Base):
    """
    Representa una operación ejecutada: compra o venta.
    Puede ser producto de una estrategia o arbitraje.
    """

    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)                      # Ej: "BTCUSDT"
    side = Column(String)                                    # "BUY" o "SELL"
    quantity = Column(Float)
    price = Column(Float)
    strategy = Column(String)                                # Nombre de la estrategia que ejecutó la operación
    result = Column(JSON, nullable=True)                     # Respuesta completa de Binance o resumen
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
