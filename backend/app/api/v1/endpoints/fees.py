from fastapi import APIRouter, HTTPException
from typing import Optional
from app.services.binance_client import BinanceClient

router = APIRouter(prefix="/fees", tags=["Fees"])

client = BinanceClient()

@router.get("/trade")
def get_trade_fees(symbol: Optional[str] = None):
    """Devuelve las comisiones de trading para los pares."""
    try:
        fees = client.get_trade_fees(symbol)
        return fees
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener comisiones: {str(e)}")
