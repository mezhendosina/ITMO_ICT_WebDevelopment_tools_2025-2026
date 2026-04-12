"""Lab 2 Task 1 — multiprocessing.Pool + partial sums."""

from __future__ import annotations

import time
from multiprocessing import Pool, cpu_count

from task1_common import chunk_bounds, inclusive_range_sum, parse_task1_args


def calculate_sum(lo: int, hi: int) -> int:
    """Compute sum of integers in [lo, hi] (single subtask)."""
    return inclusive_range_sum(lo, hi)


def _worker(pair: tuple[int, int]) -> int:
    lo, hi = pair
    return calculate_sum(lo, hi)


def main() -> None:
    args = parse_task1_args()
    bounds = [(lo, hi) for lo, hi in chunk_bounds(args.upper, args.workers) if lo <= hi]
    procs = min(args.workers, cpu_count() or 1)
    t0 = time.perf_counter()
    with Pool(processes=procs) as pool:
        parts = pool.map(_worker, bounds)
    total = sum(parts)
    elapsed = time.perf_counter() - t0
    expected = inclusive_range_sum(1, args.upper)
    print(f"multiprocessing: N={args.upper} pool={procs} chunks={len(bounds)}")
    print(f"result={total} expected={expected} ok={total == expected}")
    print(f"elapsed_sec={elapsed:.6f}")


if __name__ == "__main__":
    main()
