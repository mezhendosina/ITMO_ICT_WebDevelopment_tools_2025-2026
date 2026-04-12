"""Shared helpers for Lab 2 Task 1 (parallel partial sums over 1..N)."""

from __future__ import annotations

import argparse
from typing import List, Tuple


def inclusive_range_sum(lo: int, hi: int) -> int:
    """Sum of integers from lo to hi inclusive using Gauss's formula."""
    if lo > hi:
        return 0

    def tri(n: int) -> int:
        return n * (n + 1) // 2

    return tri(hi) - tri(lo - 1)


def chunk_bounds(n: int, parts: int) -> List[Tuple[int, int]]:
    """Split inclusive range [1, n] into `parts` contiguous subranges (as equal as possible)."""
    if n < 1:
        raise ValueError("n must be >= 1")
    if parts < 1:
        raise ValueError("parts must be >= 1")

    bounds: List[Tuple[int, int]] = []
    base = n // parts
    rem = n % parts
    start = 1
    for i in range(parts):
        size = base + (1 if i < rem else 0)
        if size <= 0:
            bounds.append((start, start - 1))
            continue
        end = start + size - 1
        bounds.append((start, end))
        start = end + 1
    return bounds


def parse_task1_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Lab 2 Task 1 — parallel sum 1..N (closed-form chunks)")
    p.add_argument(
        "-n",
        "--upper",
        type=int,
        default=10_000_000_000_000,
        help="Upper bound N for sum 1..N (default matches assignment readme)",
    )
    p.add_argument(
        "-w",
        "--workers",
        type=int,
        default=8,
        help="Number of parallel workers / chunks",
    )
    return p.parse_args()
