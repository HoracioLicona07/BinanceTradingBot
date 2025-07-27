# backend/app/market_data.py

import asyncio
from app.clients.binance_ws import BinanceWebSocketClient
from app.strategies.momentum import run_momentum_strategy
from app.logger import logger


class MarketDataManager:
    def __init__(self, symbol="btcusdt", interval="1m"):
        self.symbol = symbol.lower()
        self.interval = interval
        self.ws_client = BinanceWebSocketClient(symbol=self.symbol, interval=self.interval, callback=self.handle_data)

    async def handle_data(self, data: dict):
        """
        Callback que se ejecuta cuando llegan datos desde el WebSocket de Binance.
        """
        logger.info(f"📈 Data recibida: {data}")
        await run_momentum_strategy(data)

    async def start(self):
        logger.info("🚀 Iniciando conexión a WebSocket de Binance...")
        await self.ws_client.connect()


async def main():
    manager = MarketDataManager(symbol="btcusdt", interval="1m")
    await manager.start()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("🛑 Interrumpido por el usuario")
