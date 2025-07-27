# backend/app/core/logger.py

from loguru import logger
import sys
import os
from datetime import datetime

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, f"tradingbot_{datetime.utcnow().date()}.log")

# Crear el directorio si no existe
os.makedirs(LOG_DIR, exist_ok=True)

# Configuración base del logger
logger.remove()  # Elimina cualquier configuración previa

logger.add(sys.stdout, level="INFO", format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")

logger.add(LOG_FILE, 
           rotation="1 week", 
           retention="1 month", 
           level="DEBUG", 
           compression="zip",
           format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}")

# Ejemplo de log (puedes borrar esta línea si no la necesitas)
logger.info("Logger initialized ✅")
