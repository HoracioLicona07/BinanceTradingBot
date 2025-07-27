# backend/app/db/models/performance_log.py

from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.sql import func
from app.db.session import Base


class PerformanceLog(Base):
    """
    Registra snapshots de rendimiento del bot o de estrategias específicas.
    """

    __tablename__ = "performance_logs"

    id = Column(Integer, primary_key=True, index=True)
    strategy = Column(String, nullable=True, index=True)  # Si es null, representa global (todo el bot)
    period_days = Column(Integer, default=1)
    pnl_usd = Column(Float)
    total_trades = Column(Integer)
    meta_info = Column(JSON, nullable=True)  # ✅ Cambiado de 'metadata'
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
