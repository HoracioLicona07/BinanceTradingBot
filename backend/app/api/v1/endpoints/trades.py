# backend/app/api/v1/endpoints/trades.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.schemas.trade import TradeCreate, TradeResponse
from app.db.crud.trade import create_trade, get_trades, get_trade_by_id
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=TradeResponse)
def create_trade_endpoint(trade_data: TradeCreate, db: Session = Depends(get_db)):
    """
    Endpoint para crear una operación de trading.
    """
    return create_trade(db=db, trade_data=trade_data)

@router.get("/", response_model=List[TradeResponse])
def get_trades_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Endpoint para obtener lista de operaciones (paginadas).
    """
    return get_trades(db=db, skip=skip, limit=limit)

@router.get("/{trade_id}", response_model=TradeResponse)
def get_trade_endpoint(trade_id: int, db: Session = Depends(get_db)):
    """
    Endpoint para obtener una operación por ID.
    """
    trade = get_trade_by_id(db=db, trade_id=trade_id)
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    return trade
