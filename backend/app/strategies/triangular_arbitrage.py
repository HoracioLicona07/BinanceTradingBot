# backend/app/strategies/triangular_arbitrage.py

from app.strategies.base import BaseStrategy
from loguru import logger


class TriangularArbitrage(BaseStrategy):
    """
    Estrategia de arbitraje triangular básica:
    A -> B -> C -> A
    Requiere tres símbolos que cierren el ciclo.
    """

    def __init__(self, config, executor):
        super().__init__(config, executor)

        self.symbol_ab = config.params.get("symbol_ab", "BTCUSDT")
        self.symbol_bc = config.params.get("symbol_bc", "USDTETH")
        self.symbol_ca = config.params.get("symbol_ca", "ETHBTC")

        self.threshold = float(config.params.get("threshold", 0.5))  # % mínimo de ganancia
        self.start_quantity = float(config.quantity or 0.001)

    def run(self):
        logger.info(f"🔺 Ejecutando arbitraje triangular: {self.symbol_ab} → {self.symbol_bc} → {self.symbol_ca}")

        try:
            # Paso 1: A -> B
            price_ab = float(self.client.get_price(self.symbol_ab)["price"])  # A en B
            # Paso 2: B -> C
            price_bc = float(self.client.get_price(self.symbol_bc)["price"])  # B en C
            # Paso 3: C -> A
            price_ca = float(self.client.get_price(self.symbol_ca)["price"])  # C en A

            # Calcular resultado final si ejecutamos el ciclo completo
            amount_b = self.start_quantity * price_ab          # A → B
            amount_c = amount_b / price_bc                    # B → C
            final_a = amount_c * price_ca                     # C → A

            gain_percent = ((final_a - self.start_quantity) / self.start_quantity) * 100

            logger.info(f"🔄 Resultado A final: {final_a:.6f}, Ganancia: {gain_percent:.2f}%")

            if gain_percent >= self.threshold:
                logger.success("🟢 Oportunidad detectada: Ejecutar ciclo triangular")

                # Aquí podrías usar self.executor para ejecutar las tres órdenes
                # self.executor.buy_market(self.symbol_ab, self.start_quantity)
                # self.executor.sell_market(self.symbol_bc, amount_b)
                # self.executor.sell_market(self.symbol_ca, amount_c)

                logger.warning("⚠️ Orden real omitida: simulado para pruebas. Descomenta para operar en vivo.")
            else:
                logger.info("⏸️ No hay ganancia suficiente para arbitraje triangular.")
        except Exception as e:
            logger.error(f"❌ Error al ejecutar arbitraje triangular: {e}")
