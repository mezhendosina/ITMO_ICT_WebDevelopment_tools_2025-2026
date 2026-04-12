"""Load Lab 1 settings and build a SQLAlchemy/SQLModel engine for Lab 2 scripts."""

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


# Ensure `import app...` works when Lab 2 scripts import `l2_db` first.
prepend_lr1_to_syspath()
