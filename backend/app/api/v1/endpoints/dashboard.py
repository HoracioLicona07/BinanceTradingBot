# backend/app/api/v1/endpoints/dashboard.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db

from app.db.crud import performance, trade, arbitrage
from datetime import datetime

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/")
def get_dashboard_data(db: Session = Depends(get_db)):
    """
    Devuelve información resumen para el dashboard del bot.
    """
    latest_pnl = performance.get_latest_log(db)
    recent_trades = trade.get_recent_trades(db, limit=5)
    recent_arbitrages = arbitrage.get_recent_arbitrage_logs(db, limit=5)

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "pnl": {
            "strategy": latest_pnl.strategy if latest_pnl else None,
            "value_usd": latest_pnl.pnl_usd if latest_pnl else 0.0,
            "period_days": latest_pnl.period_days if latest_pnl else 0,
            "total_trades": latest_pnl.total_trades if latest_pnl else 0,
            "metadata": latest_pnl.metadata if latest_pnl else {}
        },
        "recent_trades": [
            {
                "id": t.id,
                "symbol": t.symbol,
                "side": t.side,
                "qty": t.quantity,
                "price": t.price,
                "timestamp": t.timestamp
            } for t in recent_trades
        ],
        "recent_arbitrage_logs": [
            {
                "id": a.id,
                "type": a.arbitrage_type,
                "symbol": a.symbol,
                "profit_usd": a.profit_usd,
                "timestamp": a.timestamp
            } for a in recent_arbitrages
        ]
    }
