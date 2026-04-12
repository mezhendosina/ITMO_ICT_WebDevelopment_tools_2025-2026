"""Lab 2 Task 1 — asyncio + asyncio.to_thread for chunk sums."""

from __future__ import annotations

import asyncio
import time

from task1_common import chunk_bounds, inclusive_range_sum, parse_task1_args


def calculate_sum(lo: int, hi: int) -> int:
    """Compute sum of integers in [lo, hi] (single subtask)."""
    return inclusive_range_sum(lo, hi)


async def main_async(upper: int, workers: int) -> tuple[int, float]:
    bounds = [(lo, hi) for lo, hi in chunk_bounds(upper, workers) if lo <= hi]
    t0 = time.perf_counter()
    tasks = [asyncio.to_thread(calculate_sum, lo, hi) for lo, hi in bounds]
    parts = await asyncio.gather(*tasks)
    elapsed = time.perf_counter() - t0
    return sum(parts), elapsed


def main() -> None:
    args = parse_task1_args()
    total, elapsed = asyncio.run(main_async(args.upper, args.workers))
    expected = inclusive_range_sum(1, args.upper)
    print(f"asyncio: N={args.upper} workers={args.workers}")
    print(f"result={total} expected={expected} ok={total == expected}")
    print(f"elapsed_sec={elapsed:.6f}")


if __name__ == "__main__":
    main()
