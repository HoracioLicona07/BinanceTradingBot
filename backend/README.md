# 🤖 BinanceTradingBot – Backend

Bot profesional de trading y arbitraje para Binance desarrollado con **FastAPI**, **SQLAlchemy** y estrategias modulares. Compatible tanto con entorno **Testnet** como con la **API real de Binance**.

---

## 🚀 ¿Qué hace este bot?

- Ejecuta estrategias de trading (ej. EMA, RSI, MACD, Grid, etc.)
- Realiza operaciones reales o simuladas (paper trading) en Binance
- Escucha precios en tiempo real vía WebSocket
- Permite crear, consultar y trackear trades, performance y logs
- Puede integrarse fácilmente con un frontend (ej. React)
- Organizado por módulos para facilitar escalabilidad y pruebas

---

## 🧱 Estructura del backend

backend/
├── main.py
├── app/
│ ├── api/v1/endpoints/ # Rutas REST
│ ├── clients/ # WebSocket + REST Binance
│ ├── config/ # YAML para estrategias
│ ├── core/ # Logger, seguridad, config global
│ ├── db/ # Modelos ORM, CRUD, esquemas Pydantic
│ ├── services/ # Lógica central del bot
│ ├── strategies/ # Estrategias de trading
│ ├── tasks/ # Tareas programadas
│ ├── utils/ # Utilidades e indicadores
│ └── init.py
├── logs/
├── tests/
├── .env
├── README.md ← (Este archivo)
├── render.yaml
├── requirements.txt
└── start.sh

---

## 🛠️ Requisitos

- Python 3.10
- PostgreSQL
- Entorno virtual (`venv`)
- Cuenta en [Binance](https://www.binance.com) y/o [Testnet](https://testnet.binance.vision)

---

## ⚙️ Configuración

### 1. Clona el repositorio y entra al backend

```bash
cd BinanceTradingBot/backend

2. Crea y activa un entorno virtual
python -m venv venv
venv\Scripts\activate  # En Windows

3. Instala dependencias
pip install -r requirements.txt

4. Configura el archivo .env
Edita el archivo .env para seleccionar Testnet o Real:

env
# === BINANCE TESTNET (activo por defecto) ===
BINANCE_BASE_URL=https://testnet.binance.vision
BINANCE_API_KEY=TU_KEY_DE_TESTNET
BINANCE_API_SECRET=TU_SECRET_DE_TESTNET

# === BINANCE REAL (para producción) ===
# BINANCE_BASE_URL=https://api.binance.com
# BINANCE_API_KEY=TU_API_KEY_REAL
# BINANCE_API_SECRET=TU_API_SECRET_REAL

# === App Config ===
ENV=development
LOG_LEVEL=INFO

# === PostgreSQL DB ===
DATABASE_URL=postgresql://usuario:password@localhost:5432/binancebot
🔐 Nunca compartas tus llaves en público.

▶️ Cómo correr el backend
Desde backend/:

uvicorn main:app --reload
El backend estará disponible en:

http://127.0.0.1:8000
Puedes acceder a la documentación interactiva:


http://127.0.0.1:8000/docs
🧪 Pruebas rápidas
Para consultar el precio de un símbolo:

GET /api/v1/prices/symbol?symbol=BTCUSDT
Para crear un trade de prueba:

POST /api/v1/trades
{
  "symbol": "BTCUSDT",
  "side": "BUY",
  "quantity": 0.001,
  "price": 27350,
  "strategy": "ema_cross"
}
📦 Próximamente
Frontend en React

Dashboard de resultados

Monitor de rendimiento

Integración con Telegram/Slack

👨‍💻 Autor
Horacio Licona – CDMX 🇲🇽
Fullstack Developer & AI Engineer

