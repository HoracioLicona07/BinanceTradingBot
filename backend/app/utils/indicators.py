# backend/app/utils/indicators.py

import numpy as np
import pandas as pd


def calculate_ema(prices: list, period: int):
    """
    Calcula la media móvil exponencial (EMA).
    """
    if len(prices) < period:
        return []
    series = pd.Series(prices)
    return series.ewm(span=period, adjust=False).mean().tolist()


def calculate_sma(prices: list, period: int):
    """
    Calcula la media móvil simple (SMA).
    """
    if len(prices) < period:
        return []
    series = pd.Series(prices)
    return series.rolling(window=period).mean().tolist()


def calculate_macd(prices: list, fast=12, slow=26, signal=9):
    """
    Calcula el indicador MACD y la línea de señal.
    """
    if len(prices) < slow:
        return [], []

    series = pd.Series(prices)
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    return macd_line.tolist(), signal_line.tolist()


def calculate_rsi(prices: list, period: int = 14):
    """
    Calcula el indicador RSI (Relative Strength Index).
    """
    if len(prices) < period + 1:
        return []

    delta = np.diff(prices)
    gains = np.where(delta > 0, delta, 0)
    losses = np.where(delta < 0, -delta, 0)

    avg_gain = np.mean(gains[:period])
    avg_loss = np.mean(losses[:period])

    rsi = []
    for i in range(period, len(prices) - 1):
        gain = gains[i]
        loss = losses[i]

        avg_gain = (avg_gain * (period - 1) + gain) / period
        avg_loss = (avg_loss * (period - 1) + loss) / period

        if avg_loss == 0:
            rsi_value = 100
        else:
            rs = avg_gain / avg_loss
            rsi_value = 100 - (100 / (1 + rs))
        rsi.append(rsi_value)
    return rsi


def calculate_vwap(highs: list, lows: list, closes: list, volumes: list):
    """
    Calcula el indicador VWAP.
    """
    typical_price = (np.array(highs) + np.array(lows) + np.array(closes)) / 3
    vwap = np.cumsum(typical_price * volumes) / np.cumsum(volumes)
    return vwap.tolist()
