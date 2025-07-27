# backend/app/api/v1/endpoints/health.py

from fastapi import APIRouter
from datetime import datetime
import platform
import socket

router = APIRouter(prefix="/health", tags=["Health Check"])


@router.get("/")
def health_check():
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "host": socket.gethostname(),
        "system": platform.system(),
        "release": platform.release()
    }
