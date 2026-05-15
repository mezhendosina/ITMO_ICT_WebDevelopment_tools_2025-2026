"""Write parsed HTML titles into Lab 1 database (parsed_page table)."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from sqlmodel import Session, select

from app.models.parsed_page import ParsedPage


async def persist_parsed_async(engine: AsyncEngine, url: str, title: str) -> None:
    """Asynchronously upsert parsed page title into the Lab 1 parsed_page table."""
    title = (title or "")[:512]
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as session:
        stmt = select(ParsedPage).where(ParsedPage.url == url)
        result = await session.execute(stmt)
        row = result.scalars().first()
        now = datetime.utcnow()
        if row:
            row.title = title
            row.fetched_at = now
        else:
            session.add(ParsedPage(url=url, title=title, fetched_at=now))
        await session.commit()