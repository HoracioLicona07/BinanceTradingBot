# backend/app/services/performance_tracker.py

from sqlalchemy.orm import Session
from app.db.models.trade import Trade
from datetime import datetime, timedelta


def calculate_pnl(trades: list) -> float:
    """
    Calcula el profit & loss (PnL) simple de una lista de operaciones.
    Supone que se alternan BUY → SELL.
    """
    pnl = 0.0
    position = None

    for trade in trades:
        if trade.side == "BUY":
            position = trade
        elif trade.side == "SELL" and position:
            pnl += (trade.price - position.price) * position.quantity
            position = None  # Resetear para la próxima operación
    return round(pnl, 2)


def get_strategy_performance(db: Session, strategy_name: str, days: int = 7) -> dict:
    """
    Devuelve estadísticas de rendimiento para una estrategia específica en los últimos X días.
    """
    since = datetime.utcnow() - timedelta(days=days)
    trades = (
        db.query(Trade)
        .filter(Trade.strategy == strategy_name, Trade.timestamp >= since)
        .order_by(Trade.timestamp)
        .all()
    )

    if not trades:
        return {
            "strategy": strategy_name,
            "message": "No hay operaciones en este período",
        }

    pnl = calculate_pnl(trades)
    total_trades = len(trades)
    buy_trades = sum(1 for t in trades if t.side == "BUY")
    sell_trades = sum(1 for t in trades if t.side == "SELL")

    return {
        "strategy": strategy_name,
        "period_days": days,
        "pnl_usd": pnl,
        "total_trades": total_trades,
        "buy_count": buy_trades,
        "sell_count": sell_trades,
    }


def get_overall_performance(db: Session, days: int = 7) -> dict:
    """
    Devuelve el rendimiento general del bot (todas las estrategias).
    """
    since = datetime.utcnow() - timedelta(days=days)
    trades = (
        db.query(Trade)
        .filter(Trade.timestamp >= since)
        .order_by(Trade.timestamp)
        .all()
    )

    if not trades:
        return {
            "message": "No hay operaciones en este período",
        }

    pnl = calculate_pnl(trades)
    strategies = list(set(t.strategy for t in trades))

    return {
        "period_days": days,
        "pnl_usd": pnl,
        "total_trades": len(trades),
        "unique_strategies": strategies,
    }
