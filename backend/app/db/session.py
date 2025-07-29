# backend/app/db/session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Conexión a la base de datos
DATABASE_URL = settings.DATABASE_URL

# Validación explícita
if not DATABASE_URL or not DATABASE_URL.startswith("postgresql"):
    raise ValueError(f"❌ DATABASE_URL inválida o vacía: '{DATABASE_URL}'")

print("🔗 Conectando a la base de datos con URL:", DATABASE_URL)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=(settings.ENV == "development")  # Solo activa logs SQL en entorno local
)

# Sesiones para usar en dependencias de FastAPI
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos ORM
Base = declarative_base()

# Dependencia para FastAPI
def get_db():
    """
    Dependency para obtener la sesión de base de datos en endpoints o servicios.
    Cierra automáticamente después de cada uso.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Sesión directa para scripts como run_bot.py
def get_db_session():
    """
    Devuelve una sesión directa (no generador) para usar fuera de FastAPI.
    """
    return SessionLocal()
