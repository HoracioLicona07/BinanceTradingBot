# backend/app/db/models/strategy_config.py

from sqlalchemy import Column, Integer, String, Boolean, JSON, Float
from app.db.session import Base


class StrategyConfig(Base):
    """
    Modelo que representa una estrategia configurada para un símbolo.
    Permite que sea activada/desactivada y tenga parámetros personalizables.
    """

    __tablename__ = "strategy_config"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)                     # Nombre de la estrategia, e.g., "Momentum"
    symbol = Column(String, index=True)                   # Símbolo de trading, e.g., "BTCUSDT"
    quantity = Column(Float, nullable=False, default=0.001)  # Cantidad a operar
    params = Column(JSON, nullable=True)                  # Parámetros específicos (interval, EMA, etc.)
    is_active = Column(Boolean, default=True)             # Si está habilitada
    description = Column(String, nullable=True)           # Descripción opcional
