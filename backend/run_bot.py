# backend/run_bot.py

from app.core.logger import logger
from app.db.session import get_db_session
from app.services.strategy_runner import StrategyRunner

logger.info("🚀 Iniciando ejecución del bot de trading...")

# Obtener sesión de base de datos
db_session = get_db_session()

# Ejecutar estrategias activas
runner = StrategyRunner(db_session)
runner.execute_strategies()
