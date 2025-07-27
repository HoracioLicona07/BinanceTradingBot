# backend/app/clients/binance_ws.py

import aiohttp
import asyncio
import json
from app.core.logger import logger  

class BinanceWebSocketClient:
    def __init__(self, symbol: str, interval: str, callback):
        self.symbol = symbol.lower()
        self.interval = interval
        self.callback = callback
        self.ws_url = f"wss://stream.binance.com:9443/ws/{self.symbol}@kline_{self.interval}"

    async def connect(self):
        """
        Conecta al WebSocket de Binance y escucha eventos.
        """
        logger.info(f"🌐 Conectando a WebSocket URL: {self.ws_url}")
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(self.ws_url) as ws:
                logger.info("✅ Conexión WebSocket establecida")
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        data = json.loads(msg.data)
                        kline = data.get("k", {})
                        await self.callback(kline)
                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        logger.error(f"❌ WebSocket error: {msg.data}")
                        break
