# backend/app/api/v1/endpoints/arbitrage.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.db.schemas.arbitrage import ArbitrageLogResponse, ArbitrageLogCreate
from app.db.crud import arbitrage as crud

router = APIRouter(prefix="/arbitrage", tags=["Arbitrage Logs"])


@router.get("/", response_model=List[ArbitrageLogResponse])
def get_all_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Devuelve los registros recientes de arbitraje.
    """
    return crud.get_logs(db, skip=skip, limit=limit)


@router.get("/{log_id}", response_model=ArbitrageLogResponse)
def get_log_by_id(log_id: int, db: Session = Depends(get_db)):
    """
    Devuelve un log de arbitraje por ID.
    """
    log = crud.get_log_by_id(db, log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Log no encontrado")
    return log


@router.post("/", response_model=ArbitrageLogResponse)
def create_arbitrage_log(log_data: ArbitrageLogCreate, db: Session = Depends(get_db)):
    """
    (Opcional) Crear un log manualmente para pruebas o simulaciones.
    """
    return crud.create_log(db, log_data)
