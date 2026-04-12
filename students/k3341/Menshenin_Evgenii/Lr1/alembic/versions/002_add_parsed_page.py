"""Add parsed_page table for Lab 2 parallel HTML parsing.

Revision ID: 002
Revises: 001
Create Date: 2026-04-11

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "parsed_page",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("url", sa.String(length=2048), nullable=False),
        sa.Column("title", sa.String(length=512), nullable=False),
        sa.Column("fetched_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_parsed_page_url"), "parsed_page", ["url"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_parsed_page_url"), table_name="parsed_page")
    op.drop_table("parsed_page")
