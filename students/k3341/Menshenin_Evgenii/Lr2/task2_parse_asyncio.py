"""Lab 2 Task 2 — asyncio + aiohttp: parallel fetch/parse/save."""

from __future__ import annotations

import argparse
import asyncio
import contextvars
import time

import aiohttp
import l2_db  # noqa: F401
from bs4 import BeautifulSoup

from l2_db import get_engine
from task2_common import DEFAULT_URLS, split_equal
from task2_persist import persist_parsed

_aio_session: contextvars.ContextVar[aiohttp.ClientSession | None] = contextvars.ContextVar(
    "aio_session", default=None
)


def _extract_title(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    tag = soup.title
    if not tag:
        return ""
    return (tag.string or tag.get_text() or "").strip()


async def parse_and_save(url: str) -> str:
    """Fetch URL with aiohttp, parse <title>, persist via sync SQLModel in a thread."""
    session = _aio_session.get()
    if session is None:
        raise RuntimeError("ClientSession is not bound (internal error).")

    engine = get_engine()
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=45)) as resp:
            resp.raise_for_status()
            text = await resp.text()
        title = _extract_title(text)
    except Exception as exc:  # noqa: BLE001
        title = f"<error: {exc}>"

    await asyncio.to_thread(persist_parsed, engine, url, title)
    print(f"{url} -> {title!r}")
    return title


async def _run_shard(shard: list[str]) -> None:
    for u in shard:
        await parse_and_save(u)


async def _async_main(workers: int) -> float:
    urls = list(DEFAULT_URLS)
    shards = [s for s in split_equal(urls, workers) if s]
    get_engine()

    t0 = time.perf_counter()
    async with aiohttp.ClientSession() as session:
        token = _aio_session.set(session)
        try:
            await asyncio.gather(*(_run_shard(s) for s in shards))
        finally:
            _aio_session.reset(token)
    return time.perf_counter() - t0


def main() -> None:
    p = argparse.ArgumentParser(description="Task 2 — asyncio + aiohttp + sharded URL list")
    p.add_argument(
        "-w",
        "--workers",
        type=int,
        default=4,
        help="Number of concurrent shard tasks (each shard parses its URLs sequentially)",
    )
    args = p.parse_args()

    elapsed = asyncio.run(_async_main(args.workers))
    print(f"asyncio_task2_elapsed_sec={elapsed:.4f} urls={len(DEFAULT_URLS)} workers={args.workers}")


if __name__ == "__main__":
    main()
