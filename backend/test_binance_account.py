# backend/test_binance_account.py

import os
import time
import hmac
import hashlib
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")  # ✅ Carga el archivo .env

BASE_URL = os.getenv("BINANCE_BASE_URL")
API_KEY = os.getenv("BINANCE_API_KEY")
SECRET_KEY = os.getenv("BINANCE_API_SECRET")

if not API_KEY or not SECRET_KEY:
    raise ValueError("❌ API_KEY o SECRET_KEY no definidas en .env")

timestamp = int(time.time() * 1000)
query_string = f"timestamp={timestamp}"
signature = hmac.new(SECRET_KEY.encode(), query_string.encode(), hashlib.sha256).hexdigest()

headers = {"X-MBX-APIKEY": API_KEY}
url = f"{BASE_URL}/api/v3/account?{query_string}&signature={signature}"

response = requests.get(url, headers=headers)

print("🔐 Probando conexión con Binance Testnet...")
print("📡 URL:", url)
print("🔑 Headers:", headers)
print("🧾 Respuesta:")
print(response.json())
