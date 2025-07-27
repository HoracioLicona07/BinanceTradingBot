# backend/app/tasks/run_arbitrage.py

from app.services.binance_client import BinanceClient
from app.core.logger import logger
from app.strategies.arbitrage.spot_arbitrage import detect_spot_arbitrage
from app.strategies.arbitrage.triangular_arbitrage import detect_triangular_arbitrage
from app.db.session import get_db
from sqlalchemy.orm import Session

# Configuración de símbolos y parámetros
ARBITRAGE_SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
QUOTE_ASSET = "USDT"  # Activo base para triangular arbitrage


def run_arbitrage_task(db: Session = next(get_db())):
    """
    Ejecuta ambas estrategias de arbitraje configuradas.
    """
    logger.info("🚀 Iniciando tarea de arbitraje...")

    client = BinanceClient()

    try:
        # 1. Spot Arbitrage (entre exchanges o pares directos)
        logger.info("🔍 Ejecutando Spot Arbitrage...")
        detect_spot_arbitrage(client, ARBITRAGE_SYMBOLS, db)

        # 2. Triangular Arbitrage (dentro de un exchange)
        logger.info("🔁 Ejecutando Triangular Arbitrage...")
        detect_triangular_arbitrage(client, QUOTE_ASSET, db)

        logger.info("✅ Arbitraje completado.")
    except Exception as e:
        logger.error(f"❌ Error durante la ejecución del arbitraje: {str(e)}")
