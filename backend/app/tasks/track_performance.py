# backend/app/tasks/track_performance.py

from app.db.session import get_db
from app.db.models.performance_log import PerformanceLog
from app.crud.trade import get_trades_by_strategy
from app.crud.strategy import get_active_strategies
from app.core.logger import logger
from sqlalchemy.orm import Session
from datetime import datetime
from decimal import Decimal

def calculate_strategy_performance(strategy_id: int, db: Session) -> dict:
    """
    Calcula las métricas de rendimiento para una estrategia.
    """
    trades = get_trades_by_strategy(db, strategy_id=strategy_id)
    if not trades:
        return {}

    total_profit = Decimal("0")
    num_trades = len(trades)
    wins = 0
    losses = 0

    for trade in trades:
        pnl = Decimal(str(trade.pnl or 0))
        total_profit += pnl
        if pnl > 0:
            wins += 1
        elif pnl < 0:
            losses += 1

    win_rate = (wins / num_trades) * 100 if num_trades else 0

    return {
        "strategy_id": strategy_id,
        "total_profit": float(total_profit),
        "win_rate": round(win_rate, 2),
        "num_trades": num_trades,
        "timestamp": datetime.utcnow()
    }

def track_performance_task(db: Session = next(get_db())):
    """
    Tarea que evalúa el rendimiento de todas las estrategias activas y guarda un log.
    """
    logger.info("📊 Ejecutando tarea de seguimiento de rendimiento...")

    try:
        active_strategies = get_active_strategies(db)

        for strategy in active_strategies:
            performance_data = calculate_strategy_performance(strategy.id, db)

            if not performance_data:
                logger.warning(f"⚠️ Sin trades para la estrategia {strategy.name}")
                continue

            perf_log = PerformanceLog(
                strategy_id=performance_data["strategy_id"],
                total_profit=performance_data["total_profit"],
                win_rate=performance_data["win_rate"],
                num_trades=performance_data["num_trades"],
                timestamp=performance_data["timestamp"]
            )

            db.add(perf_log)
            db.commit()
            logger.info(f"✅ Log de rendimiento guardado para {strategy.name}")

    except Exception as e:
        logger.error(f"❌ Error al evaluar rendimiento: {e}")
