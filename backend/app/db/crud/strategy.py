# backend/app/db/crud/strategy.py

from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.models.strategy_config import StrategyConfig
from app.db.schemas.strategy import StrategyConfigCreate, StrategyConfigUpdate


def get_active_strategies(db: Session) -> List[StrategyConfig]:
    """
    Devuelve todas las estrategias activas.
    """
    return db.query(StrategyConfig).filter(StrategyConfig.is_active == True).all()


def get_strategy_by_id(db: Session, strategy_id: int) -> Optional[StrategyConfig]:
    """
    Busca una estrategia por ID.
    """
    return db.query(StrategyConfig).filter(StrategyConfig.id == strategy_id).first()


def get_strategies(db: Session, skip: int = 0, limit: int = 100) -> List[StrategyConfig]:
    """
    Devuelve todas las estrategias (activas o no) con paginación.
    """
    return db.query(StrategyConfig).offset(skip).limit(limit).all()


def create_strategy(db: Session, strategy_data: StrategyConfigCreate) -> StrategyConfig:
    """
    Crea una nueva configuración de estrategia.
    """
    new_strategy = StrategyConfig(**strategy_data.dict(), is_active=True)
    db.add(new_strategy)
    db.commit()
    db.refresh(new_strategy)
    return new_strategy


def update_strategy(db: Session, strategy_id: int, updates: StrategyConfigUpdate) -> Optional[StrategyConfig]:
    """
    Actualiza una estrategia existente.
    """
    strategy = get_strategy_by_id(db, strategy_id)
    if not strategy:
        return None

    update_data = updates.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(strategy, key, value)

    db.commit()
    db.refresh(strategy)
    return strategy
