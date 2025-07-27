"""Helpers to evaluate triangular routes based on order book snapshots."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

SLIPPAGE_PCT = 5e-4

@dataclass
class Jump:
    src: str
    dst: str
    side: str
    factor: float
    fee: float
    expected_price: float
    max_qty: float


def avg_price(levels: List[List[str]], side: str, qty: float) -> float:
    need = qty
    spent = 0.0
    got = 0.0
    for p_str, q_str in levels:
        p = float(p_str)
        q = float(q_str)
        take = min(q, need)
        if side == "BUY":
            spent += take * p
            got += take
        else:
            spent += take
            got += take * p
        need -= take
        if need <= 0:
            break
    if need > 0:
        last_px = float(levels[-1][0])
        slip_px = last_px * (1 + SLIPPAGE_PCT if side == "BUY" else 1 - SLIPPAGE_PCT)
        if side == "BUY":
            spent += need * slip_px
            got += need
        else:
            spent += need
            got += need * slip_px
    return spent / got if side == "BUY" else got / spent


def convert_step(book: Dict[str, List[List[str]]], side: str, qty: float, fee: float) -> float:
    px_raw = avg_price(book["asks" if side == "BUY" else "bids"], side, qty)
    px = px_raw * (1 + SLIPPAGE_PCT) if side == "BUY" else px_raw * (1 - SLIPPAGE_PCT)
    if side == "BUY":
        base_out = qty / px
        net_out = base_out * (1 - fee)
        return net_out / qty
    else:
        quote_out = qty * px
        net_out = quote_out * (1 - fee)
        return net_out / qty


def max_qty_until(book: Dict[str, List[List[str]]], side: str, price_cut_pct: float = 0.003) -> float:
    levels = book["asks" if side == "BUY" else "bids"]
    best = float(levels[0][0])
    limit = best * (1 + price_cut_pct if side == "BUY" else 1 - price_cut_pct)
    qty = 0.0
    for p_str, q_str in levels:
        p = float(p_str)
        q = float(q_str)
        if side == "BUY" and p > limit:
            break
        if side == "SELL" and p < limit:
            break
        qty += q
    return qty


def route_factor(order_books: Dict[str, Dict[str, List[List[str]]]], route: List[str], qty_start: float, fee_of, hourly_interest) -> Tuple[float, List[Jump]]:
    current_qty = qty_start
    jumps: List[Jump] = []
    for src, dst in zip(route, route[1:]):
        fwd = f"{src}{dst}"
        rev = f"{dst}{src}"
        if fwd in order_books:
            sym = fwd
            side = "SELL"
        elif rev in order_books:
            sym = rev
            side = "BUY"
        else:
            return 0.0, []
        fee = fee_of(sym)
        book = order_books[sym]
        max_q = max_qty_until(book, side)
        if current_qty > max_q:
            return 0.0, []
        factor_step = convert_step(book, side, current_qty, fee)
        jumps.append(
            Jump(src, dst, side, factor=factor_step, fee=fee, expected_price=avg_price(book["asks" if side=="BUY" else "bids"], side, current_qty), max_qty=max_q)
        )
        current_qty = float(f"{(current_qty * factor_step):.10f}")
    base_asset = route[0]
    interest_pct = hourly_interest(base_asset)
    factor_total = current_qty / qty_start * (1 - interest_pct)
    return factor_total, jumps


def is_profitable(factor: float, threshold: float) -> bool:
    return factor - 1 > threshold
