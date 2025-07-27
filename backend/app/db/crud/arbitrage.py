# backend/app/db/crud/arbitrage.py

from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.models.arbitrage_log import ArbitrageLog
from app.db.schemas.arbitrage import ArbitrageLogCreate


def create_log(db: Session, log_data: ArbitrageLogCreate) -> ArbitrageLog:
    """
    Crea un nuevo registro de arbitraje.
    """
    db_log = ArbitrageLog(**log_data.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


def get_logs(db: Session, skip: int = 0, limit: int = 100) -> List[ArbitrageLog]:
    """
    Devuelve los últimos registros de arbitraje.
    """
    return db.query(ArbitrageLog).order_by(ArbitrageLog.timestamp.desc()).offset(skip).limit(limit).all()


def get_log_by_id(db: Session, log_id: int) -> Optional[ArbitrageLog]:
    """
    Devuelve un log de arbitraje por su ID.
    """
    return db.query(ArbitrageLog).filter(ArbitrageLog.id == log_id).first()
