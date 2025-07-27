# backend/app/strategies/scalping.py

from statistics import stdev
from app.strategies.base import BaseStrategy
from loguru import logger


class Scalping(BaseStrategy):
    """
    Estrategia de scalping básica basada en volatilidad.
    Compra si el precio sube mucho respecto al promedio,
    vende si cae bruscamente.
    """

    def __init__(self, config, executor):
        super().__init__(config, executor)

        self.interval = config.params.get("interval", "1m")
        self.limit = int(config.params.get("limit", 20))  # número de velas a analizar
        self.volatility_factor = float(config.params.get("volatility_factor", 1.5))  # sensibilidad

    def run(self):
        logger.info(f"🚀 Ejecutando estrategia Scalping en {self.symbol}")

        try:
            candles = self.client.client.get_klines(
                symbol=self.symbol,
                interval=self.interval,
                limit=self.limit
            )
            closes = [float(candle[4]) for candle in candles]
            current_price = closes[-1]

            if len(closes) < 5:
                logger.warning("📉 No hay suficientes datos para scalping.")
                return

            recent_volatility = stdev(closes[-5:])
            avg_price = sum(closes[-5:]) / 5

            # Señal de compra
            if current_price > avg_price + self.volatility_factor * recent_volatility:
                logger.info("📈 Señal de COMPRA rápida (breakout positivo)")
                self.executor.buy_market(self.symbol, self.quantity)

            # Señal de venta
            elif current_price < avg_price - self.volatility_factor * recent_volatility:
                logger.info("📉 Señal de VENTA rápida (breakout negativo)")
                self.executor.sell_market(self.symbol, self.quantity)

            else:
                logger.info("⏸️ Sin movimiento relevante. No se ejecuta orden.")

        except Exception as e:
            logger.error(f"❌ Error en Scalping: {e}")
