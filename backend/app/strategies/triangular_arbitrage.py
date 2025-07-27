"""Triangular arbitrage strategy using WebSocket order book updates."""

from __future__ import annotations

import asyncio
import json
import time
from collections import defaultdict
from typing import Dict, List

import aiohttp
from loguru import logger

from app.strategies.base import BaseStrategy
from app.strategies.triangular import (
    build_graph,
    find_cycles,
    route_factor,
    is_profitable,
)

# Strategy parameters
TOP_N_PAIRS = 300
BOOK_LIMIT = 100
PROFIT_THOLD = 1e-4
HOLD_SECONDS = 90
LIVE = False
SLEEP_BETWEEN = 5
QUANTUMS_USDT = [50, 100, 250, 500, 1000, 2500, 5000]


class DepthStream:
    """Lightweight Binance depth WebSocket."""

    def __init__(self, symbols: List[str], callback):
        self.symbols = [s.lower() for s in symbols]
        self.callback = callback
        streams = "/".join(f"{s}@depth@100ms" for s in self.symbols)
        self.url = f"wss://stream.binance.com:9443/stream?streams={streams}"

    async def run(self):
        logger.info(f"🌐 Conectando a {self.url}")
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(self.url) as ws:
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        data = json.loads(msg.data)
                        stream = data.get("stream", "")
                        symbol = stream.split("@")[0].upper()
                        book = data.get("data", {})
                        await self.callback(symbol, book)
                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        logger.error(f"WebSocket error: {msg.data}")
                        break


class TriangularArbitrage(BaseStrategy):
    """Scan Binance for triangular arbitrage opportunities."""

    def __init__(self, config, executor):
        super().__init__(config, executor)
        self.books: Dict[str, dict] = {}
        self.symbols: List[str] = []
        self.coins: List[str] = []
        self.balances: defaultdict[str, float] = defaultdict(float)
        self._commission_cache: Dict[str, float] = {}
        self._interest_cache: Dict[str, float] = {}

    # ---------------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------------
    def _fee_of(self, symbol: str) -> float:
        if symbol in self._commission_cache:
            return self._commission_cache[symbol]
        try:
            data = self.client.client.get_trade_fee(symbol=symbol)
            taker = float(data[0].get("taker", data[0].get("takerCommission", 0.001)))
        except Exception as exc:
            logger.warning(f"No pude obtener comisiones de {symbol} ({exc}); uso 0.001")
            taker = 0.001
        self._commission_cache[symbol] = taker
        return taker

    def _hourly_interest(self, asset: str) -> float:
        return self._interest_cache.setdefault(asset, 0.0)

    def _account_balances(self) -> Dict[str, float]:
        info = self.client.get_account_info() or {}
        balances = info.get("balances", [])
        return {b["asset"]: float(b["free"]) for b in balances if float(b["free"]) > 0}

    def _top_symbols(self, n: int) -> List[str]:
        tickers = self.client.client.get_ticker_24hr()
        tickers.sort(key=lambda d: float(d.get("quoteVolume", 0)), reverse=True)
        return [d["symbol"] for d in tickers[:n]]

    def _exchange_map(self) -> Dict[str, tuple[str, str]]:
        info = self.client.client.get_exchange_info()
        return {
            s["symbol"]: (s["baseAsset"], s["quoteAsset"])
            for s in info.get("symbols", [])
            if s.get("status") == "TRADING"
        }

    def _snapshot_books(self, symbols: List[str]) -> Dict[str, dict]:
        return {sym: self.client.client.get_order_book(symbol=sym, limit=BOOK_LIMIT) for sym in symbols}

    # ---------------------------------------------------------------
    def _prepare(self):
        sym_map = self._exchange_map()
        self.symbols = self._top_symbols(TOP_N_PAIRS)
        self.coins = list({c for s in self.symbols if s in sym_map for c in sym_map[s]})
        self.books = self._snapshot_books(self.symbols)
        self.balances = defaultdict(float, self._account_balances())

    def _build_routes(self) -> List[List[str]]:
        graph = build_graph(self.books, self._exchange_map())
        routes = find_cycles(graph, self.coins, max_hops=4)
        return routes

    def _evaluate(self, routes: List[List[str]]):
        for route in routes:
            first_asset = route[0]
            px = None
            quants = QUANTUMS_USDT
            if first_asset != "USDT":
                if f"{first_asset}USDT" in self.books:
                    px = float(self.books[f"{first_asset}USDT"]["bids"][0][0])
                elif f"USDT{first_asset}" in self.books:
                    px = 1 / float(self.books[f"USDT{first_asset}"]["asks"][0][0])
                else:
                    continue
                quants = [q / px for q in QUANTUMS_USDT]
            for qty in quants:
                factor, jumps = route_factor(
                    self.books, route, qty, self._fee_of, self._hourly_interest
                )
                if factor == 0:
                    continue
                if is_profitable(factor, PROFIT_THOLD):
                    gain_pct = (factor - 1) * 100
                    usd_equiv = qty if first_asset == "USDT" else qty * (px or 0)
                    jump_str = " → ".join(f"{j.src}->{j.dst}" for j in jumps)
                    logger.success(
                        f"💰 Ruta {jump_str} | size≈{usd_equiv:.0f} USDT | +{gain_pct:.3f}%"
                    )
                    if LIVE:
                        logger.warning("🔴 LIVE no implementado")
                else:
                    break

    async def _on_depth(self, symbol: str, data: dict):
        if "bids" in data and "asks" in data:
            self.books[symbol] = {"bids": data["bids"], "asks": data["asks"]}
            routes = self._build_routes()
            self._evaluate(routes)

    async def _scan(self):
        self._prepare()
        stream = DepthStream(self.symbols, self._on_depth)
        await stream.run()

    def run(self):
        logger.info("🔺 Escaneo de arbitraje triangular (WS)")
        start = time.time()
        try:
            asyncio.run(self._scan())
        except Exception as exc:
            logger.error(f"Error en arbitraje triangular: {exc}")
        finally:
            logger.info("⏱️ Duración %.2fs", time.time() - start)
