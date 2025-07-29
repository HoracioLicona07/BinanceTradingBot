# backend/create_tables.py

from app.db.session import engine, Base
from app.db.models.strategy_config import StrategyConfig  # ✅ Corrección aquí

def create_all_tables():
    print("🛠️ Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas correctamente.")

if __name__ == "__main__":
    create_all_tables()
