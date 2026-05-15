"""Lab 2 Task 2 — threading: parallel HTTP fetch + parse + save to Lab 1 DB."""

from __future__ import annotations

import argparse
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import l2_db  # noqa: F401 — registers Lr1 on sys.path
import requests
from bs4 import BeautifulSoup

from l2_db import get_async_engine
from task2_common import DEFAULT_URLS, split_equal
from task2_persist import persist_parsed_async


def _extract_title(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    tag = soup.title
    if not tag:
        return ""
    return (tag.string or tag.get_text() or "").strip()


def parse_and_save(url: str) -> str:
    """Fetch URL, parse <title>, persist row in `parsed_page`, print result."""
    engine = get_async_engine()
    try:
        resp = requests.get(url, timeout=45)
        resp.raise_for_status()
        title = _extract_title(resp.text)
    except Exception as exc:  # noqa: BLE001 — demo script: record failure
        title = f"<error: {exc}>"
    asyncio.run(persist_parsed_async(engine, url, title))
    print(f"{url} -> {title!r}")
    return title


def _run_shard(shard: list[str]) -> None:
    for u in shard:
        parse_and_save(u)


def main() -> None:
    p = argparse.ArgumentParser(description="Task 2 — threading + sharded URL list")
    p.add_argument("-w", "--workers", type=int, default=4, help="Number of worker threads / shards")
    args = p.parse_args()

    get_async_engine()  # fail fast if DATABASE_URL missing
    urls = list(DEFAULT_URLS)
    shards = split_equal(urls, args.workers)

    t0 = time.perf_counter()
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(_run_shard, s) for s in shards if s]
        for f in as_completed(futures):
            f.result()
    elapsed = time.perf_counter() - t0
    print(f"threading_task2_elapsed_sec={elapsed:.4f} urls={len(urls)} workers={args.workers}")


if __name__ == "__main__":
    main()
