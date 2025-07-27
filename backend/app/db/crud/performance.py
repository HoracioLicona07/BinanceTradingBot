# backend/app/db/crud/performance.py

from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.models.performance_log import PerformanceLog
from app.db.schemas.performance import PerformanceLogCreate


def create_performance_log(db: Session, log_data: PerformanceLogCreate) -> PerformanceLog:
    """
    Crea y guarda un nuevo log de rendimiento.
    """
    db_log = PerformanceLog(**log_data.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


def get_all_logs(db: Session, skip: int = 0, limit: int = 100) -> List[PerformanceLog]:
    """
    Devuelve todos los logs de rendimiento (paginados).
    """
    return db.query(PerformanceLog).order_by(PerformanceLog.timestamp.desc()).offset(skip).limit(limit).all()


def get_logs_by_strategy(db: Session, strategy: str, skip: int = 0, limit: int = 100) -> List[PerformanceLog]:
    """
    Devuelve logs filtrados por estrategia (paginados).
    """
    return (
        db.query(PerformanceLog)
        .filter(PerformanceLog.strategy == strategy)
        .order_by(PerformanceLog.timestamp.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_latest_log(db: Session, strategy: Optional[str] = None) -> Optional[PerformanceLog]:
    """
    Devuelve el log más reciente para una estrategia o del bot en general (si strategy es None).
    """
    query = db.query(PerformanceLog).order_by(PerformanceLog.timestamp.desc())
    if strategy:
        query = query.filter(PerformanceLog.strategy == strategy)
    return query.first()
