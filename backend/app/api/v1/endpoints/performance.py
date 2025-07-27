# backend/app/api/v1/endpoints/performance.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.db.schemas.performance import PerformanceLogCreate, PerformanceLogResponse
from app.db.crud import performance as crud

router = APIRouter(prefix="/performance", tags=["Performance"])


@router.post("/", response_model=PerformanceLogResponse)
def create_performance_log(log_data: PerformanceLogCreate, db: Session = Depends(get_db)):
    """
    Guarda un nuevo snapshot de rendimiento.
    """
    return crud.create_performance_log(db, log_data)


@router.get("/", response_model=List[PerformanceLogResponse])
def get_all_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Devuelve todos los logs de rendimiento (paginados).
    """
    return crud.get_all_logs(db, skip=skip, limit=limit)


@router.get("/strategy/{strategy}", response_model=List[PerformanceLogResponse])
def get_logs_by_strategy(strategy: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Devuelve los logs de una estrategia específica.
    """
    return crud.get_logs_by_strategy(db, strategy, skip=skip, limit=limit)


@router.get("/latest/", response_model=PerformanceLogResponse)
def get_latest_log(strategy: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Devuelve el último log registrado (de una estrategia o global).
    """
    log = crud.get_latest_log(db, strategy)
    if not log:
        raise HTTPException(status_code=404, detail="No se encontró log reciente.")
    return log
