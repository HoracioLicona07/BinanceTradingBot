# backend/app/services/arbitrage_engine.py

from app.db.crud.strategy import get_active_strategies
from app.services.order_executor import OrderExecutor
from app.db.session import get_db
from app.strategies import STRATEGY_REGISTRY
from sqlalchemy.orm import Session
from loguru import logger


ARBITRAGE_STRATEGIES = {"SpotArbitrage", "TriangularArbitrage"}


class ArbitrageEngine:
    """
    Ejecuta todas las estrategias activas de tipo arbitraje.
    Puede ser llamada desde una tarea programada o manualmente.
    """

    def __init__(self, db: Session):
        self.db = db
        self.executor = OrderExecutor()

    def run(self):
        logger.info("🔁 Iniciando motor de arbitraje...")
        strategies = get_active_strategies(self.db)

        for strategy in strategies:
            if strategy.name not in ARBITRAGE_STRATEGIES:
                continue

            strategy_class = STRATEGY_REGISTRY.get(strategy.name)
            if not strategy_class:
                logger.warning(f"⚠️ Estrategia {strategy.name} no registrada")
                continue

            try:
                logger.info(f"🚀 Ejecutando estrategia de arbitraje: {strategy.name} para {strategy.symbol}")
                instance = strategy_class(config=strategy, executor=self.executor)
                instance.run()
            except Exception as e:
                logger.error(f"❌ Error en {strategy.name} ({strategy.symbol}): {e}")
