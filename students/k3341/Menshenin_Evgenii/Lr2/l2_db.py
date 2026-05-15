"""Load Lab 1 settings and build SQLAlchemy/SQLModel engines for Lab 2 scripts."""

from __future__ import annotations

import sys
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv


def lr1_root() -> Path:
    return Path(__file__).resolve().parent.parent / "Lr1"


def prepend_lr1_to_syspath() -> None:
    root = str(lr1_root())
    if root not in sys.path:
        sys.path.insert(0, root)


@lru_cache(maxsize=1)
def get_engine():
    """Single process-wide engine (thread-safe for PostgreSQL via SQLAlchemy pool)."""
    prepend_lr1_to_syspath()
    load_dotenv(lr1_root() / ".env")

    from sqlmodel import create_engine

    from app.core.config import settings

    if not settings.DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL is not set. Create Lr1/.env from Lr1/.env.example and run alembic upgrade."
        )

    url = settings.DATABASE_URL
    connect_args: dict = {}
    if url.startswith("sqlite"):
        connect_args["check_same_thread"] = False

    return create_engine(
        url,
        connect_args=connect_args,
        pool_pre_ping=True,
    )


def make_async_database_url(url: str) -> str:
    """Convert common synchronous SQLAlchemy URLs to async-driver URLs."""
    if url.startswith("postgresql+asyncpg://"):
        return _strip_psycopg2_params(url)
    if url.startswith("postgresql+psycopg2://"):
        return _strip_psycopg2_params(
            url.replace("postgresql+psycopg2://", "postgresql+asyncpg://", 1)
        )
    if url.startswith("postgresql://"):
        return _strip_psycopg2_params(
            url.replace("postgresql://", "postgresql+asyncpg://", 1)
        )
    if url.startswith("sqlite+aiosqlite://"):
        return url
    if url.startswith("sqlite://"):
        return url.replace("sqlite://", "sqlite+aiosqlite://", 1)
    return url


def _strip_psycopg2_params(url: str) -> str:
    """Remove psycopg2/PostgreSQL-only query params that asyncpg does not support."""
    # asyncpg does not support gssencmode, gsslib, service, channel_binding, etc.
    params_to_strip = {
        "gssencmode",
        "gsslib",
        "channel_binding",
    }
    if "?" not in url:
        return url
    base, query = url.split("?", 1)
    pairs = []
    for part in query.split("&"):
        key = part.split("=", 1)[0].lower()
        if key not in params_to_strip:
            pairs.append(part)
    if pairs:
        return f"{base}?{'&'.join(pairs)}"
    return base


def get_async_engine():
    """Single process-wide async engine for Lab 2 async database writes."""
    prepend_lr1_to_syspath()
    load_dotenv(lr1_root() / ".env")

    from sqlalchemy.ext.asyncio import create_async_engine

    from app.core.config import settings

    if not settings.DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL is not set. Create Lr1/.env from Lr1/.env.example and run alembic upgrade."
        )

    return create_async_engine(
        make_async_database_url(settings.DATABASE_URL),
        pool_pre_ping=True,
    )


# Ensure `import app...` works when Lab 2 scripts import `l2_db` first.
prepend_lr1_to_syspath()
