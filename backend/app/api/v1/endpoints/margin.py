from fastapi import APIRouter, HTTPException
from typing import Optional
from app.services.binance_client import BinanceClient

router = APIRouter(prefix="/margin", tags=["Margin"])

client = BinanceClient()

@router.get("/interest")
def get_cross_margin_interest(asset: Optional[str] = None):
    """Devuelve las tasas de interés de cross margin."""
    try:
        data = client.get_cross_margin_interest(asset)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener interés: {str(e)}")
