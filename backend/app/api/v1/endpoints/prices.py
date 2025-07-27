# backend/app/api/v1/endpoints/prices.py

from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from app.services.binance_client import BinanceClient

router = APIRouter(prefix="/prices", tags=["Market Data"])

# Instancia compartida del cliente de Binance
client = BinanceClient()

@router.get("/ticker")
def get_price(symbol: str = Query(..., example="BTCUSDT")):
    """
    Devuelve el precio actual de un símbolo (ej: BTCUSDT).
    """
    try:
        data = client.get_price(symbol)
        return {
            "symbol": data["symbol"],
            "price": float(data["price"])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener precio: {str(e)}")


@router.get("/multiple")
def get_multiple_prices(symbols: List[str] = Query(..., example=["BTCUSDT", "ETHUSDT"])):
    """
    Devuelve los precios actuales de varios símbolos.
    """
    try:
        results = []
        for sym in symbols:
            price = client.get_price(sym)
            results.append({
                "symbol": sym,
                "price": float(price["price"])
            })
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener precios: {str(e)}")
