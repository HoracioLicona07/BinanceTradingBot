import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

# ✅ Cargar correctamente .env desde la raíz del backend
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

print("✅ ENV_PATH usado:", ENV_PATH)
print("✅ DATABASE_URL cargada desde .env:", os.getenv("DATABASE_URL"))

class Settings:
    ENV: str = os.getenv("ENV", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    BOT_NAME: str = os.getenv("BOT_NAME", "BinanceTradingBot")

    BINANCE_API_KEY: str = os.getenv("BINANCE_API_KEY")
    BINANCE_API_SECRET: str = os.getenv("BINANCE_API_SECRET")
    BINANCE_BASE_URL: str = os.getenv("BINANCE_BASE_URL")  # ✅ AÑADIDO AQUÍ

    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    DEFAULT_SYMBOL: str = os.getenv("DEFAULT_SYMBOL", "BTCUSDT")
    DEFAULT_EXCHANGE: str = os.getenv("DEFAULT_EXCHANGE", "SPOT")

    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", 8000))

    ENABLE_TELEGRAM: bool = os.getenv("ENABLE_TELEGRAM", "false").lower() == "true"
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID", "")

    def load_strategies(self, path: str = "app/config/strategies.yaml"):
        try:
            full_path = BASE_DIR / "backend" / path
            with open(full_path, "r") as f:
                data = yaml.safe_load(f)
            return data.get("strategies", [])
        except Exception as e:
            print(f"❌ Error loading strategies from YAML: {e}")
            return []

settings = Settings()
