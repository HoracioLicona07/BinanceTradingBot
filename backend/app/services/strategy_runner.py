# backend/app/services/strategy_runner.py

import importlib
import traceback
from loguru import logger
from app.db.models.strategy_config import StrategyConfig
from app.db.crud.strategy import get_active_strategies
from app.services.order_executor import OrderExecutor


class StrategyRunner:
    """
    Se encarga de cargar, inicializar y ejecutar las estrategias activas.
    """

    def __init__(self, db_session):
        self.db_session = db_session
        self.executor = OrderExecutor()

    def load_strategy_class(self, strategy_name: str):
        """
        Carga dinámicamente la clase de estrategia desde la carpeta strategies.
        """
        try:
            module = importlib.import_module(f"app.strategies.{strategy_name.lower()}")
            strategy_class = getattr(module, strategy_name.capitalize())
            return strategy_class
        except (ImportError, AttributeError) as e:
            logger.error(f"❌ No se pudo cargar la estrategia '{strategy_name}': {e}")
            logger.debug(traceback.format_exc())
            return None

    def execute_strategies(self):
        """
        Carga desde la base de datos las estrategias activas y las ejecuta.
        """
        logger.info("🚀 Ejecutando estrategias activas...")
        strategies = get_active_strategies(self.db_session)

        for strat_config in strategies:
            strategy_class = self.load_strategy_class(strat_config.name)
            if strategy_class:
                try:
                    instance = strategy_class(config=strat_config, executor=self.executor)
                    instance.run()
                except Exception as e:
                    logger.error(f"⚠️ Error al ejecutar la estrategia {strat_config.name}: {e}")
                    logger.debug(traceback.format_exc())
