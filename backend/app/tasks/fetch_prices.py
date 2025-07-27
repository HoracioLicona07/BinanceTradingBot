# backend/app/tasks/fetch_prices.py

from app.services.binance_client import BinanceClient
from app.core.logger import logger
from app.db.session import get_db
from sqlalchemy.orm import Session
from fastapi import Depends

# Puedes usar una lista fija o cargar desde la DB o config
SYMBOLS_TO_TRACK = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]

def fetch_prices_task(db: Session = next(get_db())):
    """
    Tarea que obtiene los últimos precios de ciertos símbolos desde Binance.
    """
    logger.info("⏳ Iniciando fetch de precios...")

    try:
        client = BinanceClient()
        prices = {}

        for symbol in SYMBOLS_TO_TRACK:
            price_data = client.get_price(symbol)
            if price_data:
                prices[symbol] = float(price_data["price"])
                logger.info(f"✅ Precio de {symbol}: {price_data['price']}")
            else:
                logger.warning(f"⚠️ No se pudo obtener el precio de {symbol}")

        return prices

    except Exception as e:
        logger.error(f"❌ Error al obtener precios: {str(e)}")
        return {}
