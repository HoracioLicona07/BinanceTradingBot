# backend/app/core/enums.py

from enum import Enum


class OrderSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderType(str, Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"


class StrategyType(str, Enum):
    MOMENTUM = "momentum"
    SCALPING = "scalping"
    GRID = "grid"
    EMA_CROSS = "ema_cross"
    RSI = "rsi"
    VWAP_REVERSION = "vwap_reversion"
    VOLUME_SPIKE = "volume_spike"
    MACD = "macd"


class ArbitrageType(str, Enum):
    SPOT = "spot_arbitrage"
    TRIANGULAR = "triangular_arbitrage"
