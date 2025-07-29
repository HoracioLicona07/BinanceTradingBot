# backend/test_env.py
from dotenv import load_dotenv
import os
from pathlib import Path

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

print("✅ DATABASE_URL =", os.getenv("DATABASE_URL"))
