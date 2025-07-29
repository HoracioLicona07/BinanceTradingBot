# backend/test_balance.py
from app.clients.binance_client import BinanceRestClient

client = BinanceRestClient()
account_info = client.get_account_info()

print("💰 Account Info:")
print(account_info)
