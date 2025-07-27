# backend/app/db/schemas/trade.py

from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime

class TradeBase(BaseModel):
    symbol: str = Field(..., example="BTCUSDT")
    side: str = Field(..., example="BUY")
    quantity: float = Field(..., example=0.002)
    price: float = Field(..., example=27350.55)
    strategy: str = Field(..., example="ema_cross")
    result: Optional[Dict] = Field(default=None)

class TradeCreate(TradeBase):
    pass

class TradeResponse(TradeBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
