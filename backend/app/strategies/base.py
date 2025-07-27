# backend/app/strategies/base.py

from abc import ABC, abstractmethod
from app.services.order_executor import OrderExecutor
from app.services.binance_client import BinanceClient
from loguru import logger


class BaseStrategy(ABC):
    """
    Clase base abstracta para todas las estrategias de trading.
    """

    def __init__(self, config, executor: OrderExecutor):
        """
        Parámetros:
        - config: instancia de StrategyConfig (modelo desde la DB)
        - executor: instancia de OrderExecutor para ejecutar órdenes
        """
        self.config = config
        self.executor = executor
        self.symbol = config.symbol.upper()
        self.quantity = float(config.quantity or 0.001)
        self.client = BinanceClient()

    @abstractmethod
    def run(self):
        """
        Método que debe implementar cada estrategia.
        """
        raise NotImplementedError("El método `run()` debe ser implementado en cada estrategia hija.")

    def log_config(self):
        logger.debug(f"⚙️ Configuración para {self.__class__.__name__}: {self.config}")
