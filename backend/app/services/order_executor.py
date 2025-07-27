# backend/app/services/order_executor.py

from app.services.binance_client import BinanceClient
from loguru import logger


class OrderExecutor:
    """
    Clase encargada de ejecutar órdenes de compra y venta en Binance usando market orders.
    Todas las estrategias deben usar esta clase para operar.
    """

    def __init__(self):
        self.client = BinanceClient()

    def buy_market(self, symbol: str, quantity: float):
        logger.info(f"📥 Ejecutando orden de COMPRA market: {symbol} x {quantity}")
        try:
            order = self.client.place_market_order(
                symbol=symbol,
                side='BUY',
                quantity=quantity
            )
            logger.success(f"Orden de COMPRA ejecutada: {order}")
            return order
        except Exception as e:
            logger.error(f"Error al ejecutar orden de compra: {e}")
            return None

    def sell_market(self, symbol: str, quantity: float):
        logger.info(f"Ejecutando orden de VENTA market: {symbol} x {quantity}")
        try:
            order = self.client.place_market_order(
                symbol=symbol,
                side='SELL',
                quantity=quantity
            )
            logger.success(f"Orden de VENTA ejecutada: {order}")
            return order
        except Exception as e:
            logger.error(f"Error al ejecutar orden de venta: {e}")
            return None
