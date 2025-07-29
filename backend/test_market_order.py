# backend/test_market_order.py

from app.clients.binance_client import BinanceRestClient

print("🚀 Probando una orden de mercado...")

client = BinanceRestClient()
symbol = "BTCUSDT"
side = "BUY"
quantity = 0.001  # Asegúrate de tener fondos suficientes en tu cuenta de testnet

response = client.place_market_order(symbol, side, quantity)

print("📄 Respuesta de la orden:")
print(response)
