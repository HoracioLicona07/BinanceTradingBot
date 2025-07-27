# backend/app/__init__.py

"""
Módulo raíz de la aplicación BinanceTradingBot.
"""

# Se pueden importar objetos clave si se desea acceso más directo
from app.core.logger import logger
from app.core.config import settings

__all__ = ["logger", "settings"]
