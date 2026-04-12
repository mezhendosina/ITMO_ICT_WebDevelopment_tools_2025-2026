"""Write parsed HTML titles into Lab 1 database (parsed_page table)."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy.engine import Engine
from sqlmodel import Session, select

from app.models.parsed_page import ParsedPage


def persist_parsed(engine: Engine, url: str, title: str) -> None:
    title = (title or "")[:512]
    with Session(engine) as session:
        stmt = select(ParsedPage).where(ParsedPage.url == url)
        row = session.exec(stmt).first()
        now = datetime.utcnow()
        if row:
            row.title = title
            row.fetched_at = now
        else:
            session.add(ParsedPage(url=url, title=title, fetched_at=now))
        session.commit()
