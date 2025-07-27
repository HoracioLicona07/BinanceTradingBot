# backend/app/utils/logger.py

from loguru import logger
import sys
import os
from pathlib import Path


def setup_logger(log_to_file: bool = True, level: str = "INFO"):
    """
    Configura el logger global del sistema.
    - Muestra logs en consola
    - (Opcional) Guarda logs en archivo rotativo
    """

    logger.remove()  # Elimina handlers por defecto

    # ➤ Log en consola
    logger.add(
        sys.stdout,
        level=level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{module}</cyan>:<cyan>{line}</cyan> - "
               "<level>{message}</level>",
        colorize=True
    )

    if log_to_file:
        logs_path = Path("logs")
        logs_path.mkdir(exist_ok=True)

        # ➤ Log en archivo rotativo (1 MB por archivo, hasta 5 archivos)
        logger.add(
            logs_path / "bot.log",
            rotation="1 MB",
            retention="5 days",
            compression="zip",
            level=level,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
        )

    logger.info("✅ Logger configurado correctamente.")
