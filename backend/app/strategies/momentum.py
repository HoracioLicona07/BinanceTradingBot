# backend/app/strategies/momentum.py

from app.services.binance_client import BinanceClient
from app.services.order_executor import OrderExecutor
from app.utils.indicators import calculate_ema
from loguru import logger


class Momentum:
    """
    Estrategia de momentum basada en cruce de medias móviles (EMA).
    Compra cuando EMA corta cruza hacia arriba a EMA larga y viceversa.
    """

    def __init__(self, config, executor: OrderExecutor):
        self.config = config
        self.symbol = config.symbol.upper()
        self.quantity = float(config.quantity or 0.001)
        self.client = BinanceClient()
        self.executor = executor

        # Parámetros de la estrategia (pueden venir de DB o hardcode)
        self.short_window = int(config.params.get("short_window", 5))
        self.long_window = int(config.params.get("long_window", 20))
        self.timeframe = config.params.get("interval", "1m")  # 1m, 5m, 15m, etc.
        self.limit = 100  # Velas históricas

    def run(self):
        logger.info(f"📊 Ejecutando estrategia Momentum en {self.symbol}...")

        # Obtener datos históricos
        candles = self.client.client.get_klines(
            symbol=self.symbol,
            interval=self.timeframe,
            limit=self.limit
        )

        closes = [float(candle[4]) for candle in candles]

        # Validación
        if len(closes) < self.long_window:
            logger.warning("⚠️ No hay suficientes datos para ejecutar la estrategia.")
            return

        # Cálculo de EMAs
        short_ema = calculate_ema(closes, self.short_window)
        long_ema = calculate_ema(closes, self.long_window)

        if not short_ema or not long_ema:
            logger.warning("⚠️ Error en el cálculo de EMAs.")
            return

        # Señal: cruce de medias
        if short_ema[-2] < long_ema[-2] and short_ema[-1] > long_ema[-1]:
            logger.info("📈 Señal de COMPRA detectada (cruce alcista)")
            self.executor.buy_market(self.symbol, self.quantity)

        elif short_ema[-2] > long_ema[-2] and short_ema[-1] < long_ema[-1]:
            logger.info("📉 Señal de VENTA detectada (cruce bajista)")
            self.executor.sell_market(self.symbol, self.quantity)

        else:
            logger.info("⏸️ Sin señal clara, no se ejecuta orden.")
