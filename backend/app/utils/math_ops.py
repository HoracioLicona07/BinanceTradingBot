# backend/app/utils/math_ops.py

from decimal import Decimal, ROUND_DOWN


def round_step(value: float, step: float) -> float:
    """
    Redondea el valor hacia abajo al múltiplo más cercano de `step`.
    Útil para ajustar cantidades a stepSize de Binance.
    """
    value_dec = Decimal(str(value))
    step_dec = Decimal(str(step))
    return float((value_dec // step_dec) * step_dec)


def calculate_percentage_diff(a: float, b: float) -> float:
    """
    Calcula la diferencia porcentual entre dos valores.
    """
    if b == 0:
        return 0.0
    return ((a - b) / b) * 100


def clamp(value: float, min_value: float, max_value: float) -> float:
    """
    Restringe un valor entre un mínimo y un máximo.
    """
    return max(min_value, min(value, max_value))
