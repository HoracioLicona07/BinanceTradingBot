# backend/app/tasks/run_strategies.py

from app.services.binance_client import BinanceClient
from app.core.logger import logger
from app.services.strategy_runner import run_strategy
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.crud.strategy import get_active_strategies
from app.schemas.strategy import StrategyConfig

def run_strategies_task(db: Session = next(get_db())):
    """
    Ejecuta todas las estrategias activas.
    """
    logger.info("📈 Ejecutando estrategias de trading...")

    try:
        client = BinanceClient()
        strategies = get_active_strategies(db)

        if not strategies:
            logger.warning("⚠️ No hay estrategias activas para ejecutar.")
            return

        for strategy_model in strategies:
            strategy_config = StrategyConfig.from_orm(strategy_model)

            try:
                logger.info(f"🚀 Ejecutando estrategia: {strategy_config.name}")
                run_strategy(client=client, strategy_config=strategy_config, db=db)
            except Exception as e:
                logger.error(f"❌ Error al ejecutar estrategia '{strategy_config.name}': {e}")

        logger.info("✅ Estrategias ejecutadas correctamente.")

    except Exception as e:
        logger.error(f"❌ Error general en ejecución de estrategias: {e}")
