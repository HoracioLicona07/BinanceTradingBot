# backend/app/strategies/grid.py

from app.strategies.base import BaseStrategy
from loguru import logger


class Grid(BaseStrategy):
    """
    Estrategia Grid Trading.
    Coloca compras y ventas en distintos niveles de precio para capturar fluctuaciones laterales.
    """

    def __init__(self, config, executor):
        super().__init__(config, executor)

        self.min_price = float(config.params.get("min_price", 25000))
        self.max_price = float(config.params.get("max_price", 30000))
        self.n_grids = int(config.params.get("n_grids", 5))
        self.interval = config.params.get("interval", "1m")
        self.grid_levels = self._generate_grids()

    def _generate_grids(self):
        """
        Genera los niveles de precio entre min_price y max_price
        """
        step = (self.max_price - self.min_price) / self.n_grids
        return [round(self.min_price + i * step, 2) for i in range(1, self.n_grids)]

    def run(self):
        logger.info(f"📐 Ejecutando estrategia Grid en {self.symbol}...")

        # Obtener precio actual
        try:
            ticker = self.client.get_price(self.symbol)
            if not ticker:
                return

            current_price = float(ticker['price'])
            logger.debug(f"📊 Precio actual: {current_price}")
        except Exception as e:
            logger.error(f"❌ Error obteniendo precio: {e}")
            return

        # Lógica simple: compra si cae a un grid, vende si sube a otro
        for level in self.grid_levels:
            if abs(current_price - level) < (level * 0.005):  # tolerancia del 0.5%
                if current_price < level:
                    logger.info(f"🟢 Grid alcanzado por debajo ({level}) → COMPRA")
                    self.executor.buy_market(self.symbol, self.quantity)
                elif current_price > level:
                    logger.info(f"🔴 Grid alcanzado por encima ({level}) → VENTA")
                    self.executor.sell_market(self.symbol, self.quantity)
                break
        else:
            logger.info("🔁 Precio fuera de zona de ejecución de rejilla.")
