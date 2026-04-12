from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class ParsedPage(SQLModel, table=True):
    """HTML pages fetched in Lab 2 (parallel parsers)."""

    __tablename__ = "parsed_page"

    id: Optional[int] = Field(default=None, primary_key=True)
    url: str = Field(index=True, max_length=2048)
    title: str = Field(default="", max_length=512)
    fetched_at: datetime = Field(default_factory=datetime.utcnow)
