# backend/app/strategies/__init__.py

from .momentum import Momentum
from .scalping import Scalping
from .grid import Grid
from .macd import Macd
from .rsi import Rsi
from .ema_cross import EmaCross
from .volume_spike import VolumeSpike
from .vwap_reversion import VwapReversion
from .spot_arbitrage import SpotArbitrage
from .triangular_arbitrage import TriangularArbitrage

# Diccionario de estrategias disponibles (referenciables por nombre)
STRATEGY_REGISTRY = {
    "Momentum": Momentum,
    "Scalping": Scalping,
    "Grid": Grid,
    "Macd": Macd,
    "Rsi": Rsi,
    "EmaCross": EmaCross,
    "VolumeSpike": VolumeSpike,
    "VwapReversion": VwapReversion,
    "SpotArbitrage": SpotArbitrage,
    "TriangularArbitrage": TriangularArbitrage,
}
