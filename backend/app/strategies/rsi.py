# backend/app/strategies/rsi.py

from app.strategies.base import BaseStrategy
from app.utils.indicators import calculate_rsi
from loguru import logger


class Rsi(BaseStrategy):
    """
    Estrategia basada en el RSI (Relative Strength Index).
    Compra si RSI < 30 (sobreventa), vende si RSI > 70 (sobrecompra).
    """

    def __init__(self, config, executor):
        super().__init__(config, executor)

        self.interval = config.params.get("interval", "15m")
        self.limit = int(config.params.get("limit", 100))
        self.period = int(config.params.get("period", 14))
        self.overbought = float(config.params.get("overbought", 70))
        self.oversold = float(config.params.get("oversold", 30))

    def run(self):
        logger.info(f"📉 Ejecutando estrategia RSI en {self.symbol}")

        try:
            candles = self.client.client.get_klines(
                symbol=self.symbol,
                interval=self.interval,
                limit=self.limit
            )
            closes = [float(candle[4]) for candle in candles]

            rsi = calculate_rsi(closes, self.period)

            if not rsi or len(rsi) < 2:
                logger.warning("⚠️ Insuficientes datos RSI")
                return

            rsi_now = rsi[-1]
            logger.info(f"🔎 RSI actual: {rsi_now:.2f}")

            if rsi_now < self.oversold:
                logger.info("📈 Señal RSI: COMPRA (sobreventa)")
                self.executor.buy_market(self.symbol, self.quantity)

            elif rsi_now > self.overbought:
                logger.info("📉 Señal RSI: VENTA (sobrecompra)")
                self.executor.sell_market(self.symbol, self.quantity)

            else:
                logger.info("⏸️ RSI en zona neutral. No se ejecuta orden.")

        except Exception as e:
            logger.error(f"❌ Error en estrategia RSI: {e}")
