# backend/app/strategies/volume_spike.py

from app.strategies.base import BaseStrategy
from loguru import logger


class VolumeSpike(BaseStrategy):
    """
    Estrategia que detecta picos de volumen inusuales para anticipar movimientos fuertes.
    Compra si volumen alto + vela alcista.
    Vende si volumen alto + vela bajista.
    """

    def __init__(self, config, executor):
        super().__init__(config, executor)

        self.interval = config.params.get("interval", "5m")
        self.limit = int(config.params.get("limit", 30))
        self.multiplier = float(config.params.get("multiplier", 2.0))  # cuánto más que el promedio debe ser

    def run(self):
        logger.info(f"📊 Ejecutando estrategia Volume Spike en {self.symbol}")

        try:
            candles = self.client.client.get_klines(
                symbol=self.symbol,
                interval=self.interval,
                limit=self.limit
            )

            volumes = [float(candle[5]) for candle in candles]
            closes = [float(candle[4]) for candle in candles]
            opens = [float(candle[1]) for candle in candles]

            # Última vela
            last_volume = volumes[-1]
            avg_volume = sum(volumes[:-1]) / (len(volumes) - 1)

            if last_volume >= self.multiplier * avg_volume:
                logger.info(f"🚨 Volumen spike detectado: {last_volume:.2f} vs promedio {avg_volume:.2f}")

                if closes[-1] > opens[-1]:
                    logger.info("📈 Cierre alcista → COMPRA")
                    self.executor.buy_market(self.symbol, self.quantity)

                elif closes[-1] < opens[-1]:
                    logger.info("📉 Cierre bajista → VENTA")
                    self.executor.sell_market(self.symbol, self.quantity)

                else:
                    logger.info("⏸️ Cierre neutro. No se ejecuta orden.")
            else:
                logger.info("✅ Sin spike de volumen. Condición no cumplida.")

        except Exception as e:
            logger.error(f"❌ Error en Volume Spike: {e}")
