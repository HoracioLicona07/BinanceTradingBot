# backend/app/db/crud/trade.py

from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.models.trade import Trade
from app.db.schemas.trade import TradeCreate


def create_trade(db: Session, trade_data: TradeCreate) -> Trade:
    """
    Guarda una operación de trading ejecutada.
    """
    db_trade = Trade(**trade_data.dict())
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    return db_trade


def get_trades(db: Session, skip: int = 0, limit: int = 100) -> List[Trade]:
    """
    Obtiene lista de operaciones ejecutadas (paginadas).
    """
    return db.query(Trade).order_by(Trade.timestamp.desc()).offset(skip).limit(limit).all()


def get_trade_by_id(db: Session, trade_id: int) -> Optional[Trade]:
    """
    Busca una operación por su ID.
    """
    return db.query(Trade).filter(Trade.id == trade_id).first()
