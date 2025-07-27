# backend/app/api/v1/endpoints/strategies.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.db.schemas.strategy import (
    StrategyConfigResponse,
    StrategyConfigCreate,
    StrategyConfigUpdate
)
from app.db.crud import strategy as crud

router = APIRouter(prefix="/strategies", tags=["Strategies"])


@router.get("/", response_model=List[StrategyConfigResponse])
def get_all_strategies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_strategies(db, skip=skip, limit=limit)


@router.get("/active", response_model=List[StrategyConfigResponse])
def get_active_strategies(db: Session = Depends(get_db)):
    return crud.get_active_strategies(db)


@router.get("/{strategy_id}", response_model=StrategyConfigResponse)
def get_strategy_by_id(strategy_id: int, db: Session = Depends(get_db)):
    strategy = crud.get_strategy_by_id(db, strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@router.post("/", response_model=StrategyConfigResponse, status_code=status.HTTP_201_CREATED)
def create_strategy(strategy_data: StrategyConfigCreate, db: Session = Depends(get_db)):
    return crud.create_strategy(db, strategy_data)


@router.patch("/{strategy_id}", response_model=StrategyConfigResponse)
def update_strategy(strategy_id: int, updates: StrategyConfigUpdate, db: Session = Depends(get_db)):
    strategy = crud.update_strategy(db, strategy_id, updates)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy
