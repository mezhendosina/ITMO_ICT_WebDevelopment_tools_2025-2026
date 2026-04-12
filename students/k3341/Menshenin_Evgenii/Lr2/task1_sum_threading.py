"""Lab 2 Task 1 — threading.ThreadPoolExecutor + partial sums."""

from __future__ import annotations

import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from task1_common import chunk_bounds, inclusive_range_sum, parse_task1_args


def calculate_sum(lo: int, hi: int) -> int:
    """Compute sum of integers in [lo, hi] (single subtask)."""
    return inclusive_range_sum(lo, hi)


def main() -> None:
    args = parse_task1_args()
    bounds = chunk_bounds(args.upper, args.workers)
    t0 = time.perf_counter()
    total = 0
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(calculate_sum, lo, hi): (lo, hi) for lo, hi in bounds if lo <= hi}
        for fut in as_completed(futures):
            total += fut.result()
    elapsed = time.perf_counter() - t0
    expected = inclusive_range_sum(1, args.upper)
    print(f"threading: N={args.upper} workers={args.workers}")
    print(f"result={total} expected={expected} ok={total == expected}")
    print(f"elapsed_sec={elapsed:.6f}")


if __name__ == "__main__":
    main()
