"""Lab 2 Task 2 — multiprocessing: parallel fetch/parse/save."""

from __future__ import annotations

import argparse
import time
from multiprocessing import Pool, cpu_count

import l2_db  # noqa: F401

import requests
from bs4 import BeautifulSoup

from l2_db import get_engine
from task2_common import DEFAULT_URLS, split_equal
from task2_persist import persist_parsed


def _extract_title(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    tag = soup.title
    if not tag:
        return ""
    return (tag.string or tag.get_text() or "").strip()


def parse_and_save(url: str) -> str:
    """Fetch URL, parse <title>, persist row in `parsed_page`, print result."""
    engine = get_engine()
    try:
        resp = requests.get(url, timeout=45)
        resp.raise_for_status()
        title = _extract_title(resp.text)
    except Exception as exc:  # noqa: BLE001
        title = f"<error: {exc}>"
    persist_parsed(engine, url, title)
    print(f"{url} -> {title!r}")
    return title


def _run_shard(shard: list[str]) -> None:
    for u in shard:
        parse_and_save(u)


def main() -> None:
    p = argparse.ArgumentParser(description="Task 2 — multiprocessing + sharded URL list")
    p.add_argument("-w", "--workers", type=int, default=4, help="Number of processes / shards")
    args = p.parse_args()

    urls = list(DEFAULT_URLS)
    procs = min(max(1, args.workers), cpu_count() or 1)
    shards = [s for s in split_equal(urls, procs) if s]

    t0 = time.perf_counter()
    with Pool(processes=procs) as pool:
        pool.map(_run_shard, shards, chunksize=1)
    elapsed = time.perf_counter() - t0
    print(f"multiprocessing_task2_elapsed_sec={elapsed:.4f} urls={len(urls)} processes={procs}")


if __name__ == "__main__":
    main()
