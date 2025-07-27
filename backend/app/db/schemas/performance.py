# backend/app/db/schemas/performance.py

from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime


class PerformanceLogBase(BaseModel):
    strategy: Optional[str] = Field(None, example="ema_cross")
    period_days: int = Field(..., example=7)
    pnl_usd: float = Field(..., example=152.35)
    total_trades: int = Field(..., example=18)
    metadata: Optional[Dict] = Field(default=None, example={"accuracy": 0.66, "sharpe_ratio": 1.12})


class PerformanceLogCreate(PerformanceLogBase):
    pass


class PerformanceLogResponse(PerformanceLogBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
