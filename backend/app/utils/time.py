# backend/app/utils/time.py

from datetime import datetime, timedelta, timezone
import pytz


def now_utc() -> datetime:
    """
    Devuelve la hora actual en UTC como datetime con zona horaria.
    """
    return datetime.now(timezone.utc)


def now_local(tz_name: str = "America/Mexico_City") -> datetime:
    """
    Devuelve la hora local en la zona horaria especificada.
    Por defecto: CDMX (UTC-6/-5)
    """
    tz = pytz.timezone(tz_name)
    return datetime.now(tz)


def to_iso(dt: datetime) -> str:
    """
    Convierte un datetime a string ISO 8601 (formato estándar).
    """
    return dt.astimezone(timezone.utc).isoformat()


def add_seconds(dt: datetime, seconds: int) -> datetime:
    """
    Suma segundos a un datetime.
    """
    return dt + timedelta(seconds=seconds)


def seconds_since(dt: datetime) -> float:
    """
    Calcula cuántos segundos han pasado desde un datetime.
    """
    return (now_utc() - dt).total_seconds()
