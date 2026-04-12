"""Shared URL list and sharding helpers for Lab 2 Task 2."""

from __future__ import annotations


# Small set of stable public pages suitable for teaching / CI (HTML + title).
DEFAULT_URLS: list[str] = [
    "https://example.com",
    "https://example.org",
    "https://httpbin.org/html",
    "https://docs.python.org/3/library/threading.html",
    "https://docs.python.org/3/library/multiprocessing.html",
    "https://docs.python.org/3/library/asyncio.html",
]


def split_equal(items: list[str], parts: int) -> list[list[str]]:
    """Split `items` into `parts` contiguous slices; sizes differ by at most one."""
    if parts < 1:
        raise ValueError("parts must be >= 1")
    n = len(items)
    if n == 0:
        return [[] for _ in range(parts)]

    base = n // parts
    rem = n % parts
    out: list[list[str]] = []
    i = 0
    for p in range(parts):
        size = base + (1 if p < rem else 0)
        out.append(items[i : i + size])
        i += size
    return out
