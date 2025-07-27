# backend/app/strategies/ema_cross.py

from app.strategies.base import BaseStrategy
from app.utils.indicators import calculate_ema
from loguru import logger


class EmaCross(BaseStrategy):
    """
    Estrategia de cruce de medias móviles exponenciales (EMA).
    Compra si la EMA corta cruza hacia arriba la EMA larga.
    Vende si la EMA corta cruza hacia abajo la EMA larga.
    """

    def __init__(self, config, executor):
        super().__init__(config, executor)

        self.interval = config.params.get("interval", "15m")
        self.limit = int(config.params.get("limit", 100))
        self.short_window = int(config.params.get("short_window", 9))
        self.long_window = int(config.params.get("long_window", 21))

    def run(self):
        logger.info(f"📈 Ejecutando estrategia EMA Cross en {self.symbol}")

        try:
            candles = self.client.client.get_klines(
                symbol=self.symbol,
                interval=self.interval,
                limit=self.limit
            )
            closes = [float(candle[4]) for candle in candles]

            if len(closes) < self.long_window:
                logger.warning("⚠️ No hay suficientes datos para calcular EMAs.")
                return

            ema_short = calculate_ema(closes, self.short_window)
            ema_long = calculate_ema(closes, self.long_window)

            if not ema_short or not ema_long:
                logger.warning("⚠️ Falló el cálculo de EMAs.")
                return

            # Evaluar cruce de EMAs (últimas dos velas)
            if ema_short[-2] < ema_long[-2] and ema_short[-1] > ema_long[-1]:
                logger.info("🟢 Cruce alcista detectado → COMPRA")
                self.executor.buy_market(self.symbol, self.quantity)

            elif ema_short[-2] > ema_long[-2] and ema_short[-1] < ema_long[-1]:
                logger.info("🔴 Cruce bajista detectado → VENTA")
                self.executor.sell_market(self.symbol, self.quantity)

            else:
                logger.info("⏸️ Sin cruce relevante de EMAs")

        except Exception as e:
            logger.error(f"❌ Error en estrategia EMA Cross: {e}")
