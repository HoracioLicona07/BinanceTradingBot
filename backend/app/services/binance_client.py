# backend/app/services/binance_client.py

import os
from dotenv import load_dotenv
from binance.client import Client
from binance.enums import ORDER_TYPE_MARKET, SIDE_BUY, SIDE_SELL
from binance.exceptions import BinanceAPIException, BinanceOrderException

load_dotenv()


class BinanceClient:
    def __init__(self):
        self.api_key = os.getenv("BINANCE_API_KEY")
        self.api_secret = os.getenv("BINANCE_API_SECRET")

        if not self.api_key or not self.api_secret:
            raise ValueError("Faltan las claves de API en el entorno (.env)")

        self.client = Client(api_key=self.api_key, api_secret=self.api_secret)

    def get_price(self, symbol: str):
        """Obtiene el precio actual del símbolo proporcionado."""
        try:
            return self.client.get_symbol_ticker(symbol=symbol)
        except BinanceAPIException as e:
            print(f"[ERROR Binance API] {e.message}")
        except Exception as e:
            print(f"[ERROR General] {e}")
        return None

    def get_account_info(self):
        """Devuelve la información de cuenta Binance (balances, permisos, etc)."""
        try:
            return self.client.get_account()
        except BinanceAPIException as e:
            print(f"[ERROR Binance API] {e.message}")
        except Exception as e:
            print(f"[ERROR General] {e}")
        return None

    def place_market_order(self, symbol: str, side: str, quantity: float):
        """
        Ejecuta una orden de mercado.
        `side`: 'BUY' o 'SELL'
        """
        try:
            order = self.client.create_order(
                symbol=symbol,
                side=SIDE_BUY if side.upper() == 'BUY' else SIDE_SELL,
                type=ORDER_TYPE_MARKET,
                quantity=quantity
            )
            return order
        except BinanceOrderException as e:
            print(f"[ERROR Orden] {e.message}")
        except BinanceAPIException as e:
            print(f"[ERROR Binance API] {e.message}")
        except Exception as e:
            print(f"[ERROR General] {e}")
        return None

    def get_open_orders(self, symbol: str = None):
        """Devuelve las órdenes abiertas, puede filtrarse por símbolo."""
        try:
            if symbol:
                return self.client.get_open_orders(symbol=symbol)
            return self.client.get_open_orders()
        except BinanceAPIException as e:
            print(f"[ERROR Binance API] {e.message}")
        except Exception as e:
            print(f"[ERROR General] {e}")
        return None

    def cancel_order(self, symbol: str, order_id: str):
        """Cancela una orden abierta en un símbolo específico."""
        try:
            return self.client.cancel_order(symbol=symbol, orderId=order_id)
        except BinanceAPIException as e:
            print(f"[ERROR Binance API] {e.message}")
        except Exception as e:
            print(f"[ERROR General] {e}")
        return None

    def get_symbol_info(self, symbol: str):
        """Obtiene información del símbolo (lotes mínimos, stepSize, etc)."""
        try:
            return self.client.get_symbol_info(symbol)
        except Exception as e:
            print(f"[ERROR get_symbol_info] {e}")
        return None
