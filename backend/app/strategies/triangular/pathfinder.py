"""Utilities for finding triangular arbitrage cycles."""

from __future__ import annotations

import heapq
from typing import Dict, List, Tuple

# Type aliases
Graph = Dict[str, Dict[str, float]]
Route = List[str]


def build_graph(order_books: Dict[str, dict], mapping: Dict[str, Tuple[str, str]]) -> Graph:
    """Builds a conversion graph from depth snapshots."""
    graph: Graph = {}
    for sym, book in order_books.items():
        if sym not in mapping:
            continue
        if not book.get("bids") or not book.get("asks"):
            continue
        base, quote = mapping[sym]
        bid_px = float(book["bids"][0][0])
        ask_px = float(book["asks"][0][0])
        fee = 0.001  # rough estimate
        graph.setdefault(base, {})[quote] = bid_px * (1 - fee)
        graph.setdefault(quote, {})[base] = (1 / ask_px) * (1 - fee)
    return graph


def best_paths_from(src: str, graph: Graph, max_hops: int = 5) -> Dict[str, Tuple[float, Route]]:
    """Variation of Dijkstra that maximizes conversion factor."""
    best: Dict[str, Tuple[float, Route]] = {src: (1.0, [src])}
    pq: List[Tuple[float, str, Route]] = [(0.0, src, [src])]

    while pq:
        cost, node, path = heapq.heappop(pq)
        hops = len(path) - 1
        if hops >= max_hops:
            continue
        for nxt, factor in graph.get(node, {}).items():
            new_factor = best[node][0] * factor
            if new_factor > best.get(nxt, (0.0, []))[0]:
                best[nxt] = (new_factor, path + [nxt])
                heapq.heappush(pq, (-(new_factor), nxt, path + [nxt]))
    return best


def find_cycles(graph: Graph, coins: List[str], max_hops: int = 4) -> List[Route]:
    """Find cycles that start and end at the same coin."""
    cycles: List[Route] = []
    for coin in coins:
        best_paths = best_paths_from(coin, graph, max_hops)
        for dst, (factor, path) in best_paths.items():
            if len(path) < 2 or len(path) > max_hops:
                continue
            last = path[-1]
            if coin in graph.get(last, {}):
                cycles.append(path + [coin])
    return cycles
