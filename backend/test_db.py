# backend/test_db.py

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")  # Cargar variables desde .env

# Mostrar la URL cargada para debug
print("🔍 URL cargada:", os.getenv("DATABASE_URL"))

try:
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    print("✅ Conexión exitosa a PostgreSQL en Render")
    conn.close()
except Exception as e:
    print(f"❌ Error al conectar: {e}")
