# backend/app/clients/binance_client.py

import os
import requests
import hmac
import hashlib
import time
from urllib.parse import urlencode
from app.core.logger import logger
from dotenv import load_dotenv
from app.core.config import settings

class BinanceRestClient:
    def __init__(self):
        self.base_url = settings.BINANCE_BASE_URL
        self.api_key = settings.BINANCE_API_KEY
        self.api_secret = settings.BINANCE_API_SECRET


#load_dotenv()  # Asegura que se carguen variables .env si no están cargadas aún

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
BINANCE_BASE_URL = os.getenv("BINANCE_BASE_URL", "https://api.binance.com")  # fallback a real

class BinanceRestClient:
    def __init__(self):
        self.base_url = BINANCE_BASE_URL
        self.api_key = BINANCE_API_KEY
        self.api_secret = BINANCE_API_SECRET

    def _get_headers(self):
        return {
            "X-MBX-APIKEY": self.api_key
        }

    def _sign_params(self, params):
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode(), query_string.encode(), hashlib.sha256
        ).hexdigest()
        return f"{query_string}&signature={signature}"

    def get_server_time(self):
        url = f"{self.base_url}/api/v3/time"
        r = requests.get(url)
        return r.json()

    def get_account_info(self):
        url = f"{self.base_url}/api/v3/account"
        timestamp = int(time.time() * 1000)
        params = {"timestamp": timestamp}
        full_query = self._sign_params(params)
        r = requests.get(f"{url}?{full_query}", headers=self._get_headers())
        return r.json()

    def get_symbol_price(self, symbol="BTCUSDT"):
        url = f"{self.base_url}/api/v3/ticker/price"
        params = {"symbol": symbol}
        r = requests.get(url, params=params)
        return r.json()

    def place_market_order(self, symbol, side, quantity):
        """
        side = 'BUY' or 'SELL'
        """
        url = f"{self.base_url}/api/v3/order"
        timestamp = int(time.time() * 1000)
        params = {
            "symbol": symbol,
            "side": side,
            "type": "MARKET",
            "quantity": quantity,
            "timestamp": timestamp
        }
        query = self._sign_params(params)
        r = requests.post(f"{url}?{query}", headers=self._get_headers())
        return r.json()
