# backend/app/db/schemas/strategy.py

from pydantic import BaseModel, Field
from typing import Optional, Dict


class StrategyConfigBase(BaseModel):
    name: str = Field(..., example="Momentum")
    symbol: str = Field(..., example="BTCUSDT")
    quantity: float = Field(..., example=0.01)
    params: Optional[Dict] = Field(default={}, example={"interval": "15m", "short_window": 9, "long_window": 21})
    description: Optional[str] = Field(default=None, example="Estrategia de cruce de EMAs")

class StrategyConfigCreate(StrategyConfigBase):
    pass

class StrategyConfigUpdate(BaseModel):
    quantity: Optional[float]
    params: Optional[Dict]
    is_active: Optional[bool]
    description: Optional[str]

class StrategyConfigResponse(StrategyConfigBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
