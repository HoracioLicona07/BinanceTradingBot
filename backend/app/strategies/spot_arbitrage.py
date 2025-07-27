# backend/app/strategies/spot_arbitrage.py

from app.strategies.base import BaseStrategy
from loguru import logger


class SpotArbitrage(BaseStrategy):
    """
    Estrategia básica de arbitraje entre dos pares spot.
    Compara precios de un activo en dos pares (por ejemplo BTC/USDT vs BTC/BUSD)
    y ejecuta compra/venta si la diferencia excede un umbral.
    """

    def __init__(self, config, executor):
        super().__init__(config, executor)

        self.pair_a = config.params.get("pair_a", "BTCUSDT")
        self.pair_b = config.params.get("pair_b", "BTCBUSD")
        self.threshold = float(config.params.get("threshold", 0.3))  # % mínimo de diferencia para actuar

        self.quantity = float(config.quantity or 0.001)

    def run(self):
        logger.info(f"🔁 Ejecutando estrategia de arbitraje entre {self.pair_a} y {self.pair_b}")

        try:
            price_a = float(self.client.get_price(self.pair_a)["price"])
            price_b = float(self.client.get_price(self.pair_b)["price"])
        except Exception as e:
            logger.error(f"❌ Error al obtener precios: {e}")
            return

        if not price_a or not price_b:
            logger.warning("⚠️ No se pudieron obtener precios válidos.")
            return

        diff_percent = abs(price_a - price_b) / ((price_a + price_b) / 2) * 100
        logger.info(f"📊 Precio {self.pair_a}: {price_a}, {self.pair_b}: {price_b}, Diferencia: {diff_percent:.2f}%")

        if diff_percent >= self.threshold:
            if price_a < price_b:
                logger.success(f"🟢 Comprar en {self.pair_a}, vender en {self.pair_b}")
                self.executor.buy_market(self.pair_a, self.quantity)
                self.executor.sell_market(self.pair_b, self.quantity)
            else:
                logger.success(f"🟢 Comprar en {self.pair_b}, vender en {self.pair_a}")
                self.executor.buy_market(self.pair_b, self.quantity)
                self.executor.sell_market(self.pair_a, self.quantity)
        else:
            logger.info("⏸️ Diferencia de precios insuficiente para arbitraje.")
