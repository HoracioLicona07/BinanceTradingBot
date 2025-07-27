# backend/app/strategies/macd.py

from app.strategies.base import BaseStrategy
from app.utils.indicators import calculate_macd
from loguru import logger


class Macd(BaseStrategy):
    """
    Estrategia basada en el cruce de la línea MACD y la línea de señal.
    Compra cuando MACD cruza hacia arriba la señal.
    Vende cuando MACD cruza hacia abajo.
    """

    def __init__(self, config, executor):
        super().__init__(config, executor)

        self.interval = config.params.get("interval", "1m")
        self.limit = int(config.params.get("limit", 100))
        self.fast = int(config.params.get("fast", 12))
        self.slow = int(config.params.get("slow", 26))
        self.signal = int(config.params.get("signal", 9))

    def run(self):
        logger.info(f"📊 Ejecutando estrategia MACD en {self.symbol}")

        try:
            candles = self.client.client.get_klines(
                symbol=self.symbol,
                interval=self.interval,
                limit=self.limit
            )
            closes = [float(candle[4]) for candle in candles]

            macd_line, signal_line = calculate_macd(closes, self.fast, self.slow, self.signal)

            if len(macd_line) < 2 or len(signal_line) < 2:
                logger.warning("⚠️ Insuficientes datos MACD")
                return

            # Cruce MACD arriba = compra
            if macd_line[-2] < signal_line[-2] and macd_line[-1] > signal_line[-1]:
                logger.info("📈 Señal MACD: COMPRA")
                self.executor.buy_market(self.symbol, self.quantity)

            # Cruce MACD abajo = venta
            elif macd_line[-2] > signal_line[-2] and macd_line[-1] < signal_line[-1]:
                logger.info("📉 Señal MACD: VENTA")
                self.executor.sell_market(self.symbol, self.quantity)

            else:
                logger.info("⏸️ Sin señal MACD clara")

        except Exception as e:
            logger.error(f"❌ Error en estrategia MACD: {e}")
