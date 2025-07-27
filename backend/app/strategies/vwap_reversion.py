# backend/app/strategies/vwap_reversion.py

from app.strategies.base import BaseStrategy
from app.utils.indicators import calculate_vwap
from loguru import logger


class VwapReversion(BaseStrategy):
    """
    Estrategia que ejecuta órdenes cuando el precio se desvía significativamente del VWAP.
    Compra si el precio está muy por debajo del VWAP (esperando reversión alcista).
    Vende si el precio está muy por encima del VWAP (esperando reversión bajista).
    """

    def __init__(self, config, executor):
        super().__init__(config, executor)

        self.interval = config.params.get("interval", "15m")
        self.limit = int(config.params.get("limit", 30))
        self.deviation_percent = float(config.params.get("deviation_percent", 1.0))  # e.g. 1.0%

    def run(self):
        logger.info(f"📏 Ejecutando estrategia VWAP Reversion en {self.symbol}")

        try:
            candles = self.client.client.get_klines(
                symbol=self.symbol,
                interval=self.interval,
                limit=self.limit
            )

            highs = [float(candle[2]) for candle in candles]
            lows = [float(candle[3]) for candle in candles]
            closes = [float(candle[4]) for candle in candles]
            volumes = [float(candle[5]) for candle in candles]

            vwap_series = calculate_vwap(highs, lows, closes, volumes)
            if not vwap_series or len(vwap_series) < 1:
                logger.warning("⚠️ VWAP insuficiente.")
                return

            current_price = closes[-1]
            current_vwap = vwap_series[-1]

            diff_pct = ((current_price - current_vwap) / current_vwap) * 100
            logger.info(f"VWAP: {current_vwap:.2f}, Precio: {current_price:.2f}, Diferencia: {diff_pct:.2f}%")

            if diff_pct <= -self.deviation_percent:
                logger.info("📈 Precio muy por debajo del VWAP → COMPRA")
                self.executor.buy_market(self.symbol, self.quantity)

            elif diff_pct >= self.deviation_percent:
                logger.info("📉 Precio muy por encima del VWAP → VENTA")
                self.executor.sell_market(self.symbol, self.quantity)

            else:
                logger.info("⏸️ Precio cerca del VWAP → no se ejecuta orden.")

        except Exception as e:
            logger.error(f"❌ Error en VWAP Reversion: {e}")
