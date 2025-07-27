# backend/app/db/schemas/arbitrage.py

from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime


class ArbitrageLogBase(BaseModel):
    strategy_name: str = Field(..., example="SpotArbitrage")
    symbol_a: str = Field(..., example="BTCUSDT")
    symbol_b: str = Field(..., example="BTCBUSD")
    price_a: float = Field(..., example=27365.12)
    price_b: float = Field(..., example=27381.75)
    percent_diff: float = Field(..., example=0.61)
    executed: str = Field(..., example="YES")
    result: Optional[Dict] = Field(default=None, example={"order_id_a": 123, "order_id_b": 456})


class ArbitrageLogCreate(ArbitrageLogBase):
    pass


class ArbitrageLogResponse(ArbitrageLogBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
