"""initial schema with skillwarriorlink.level

Revision ID: 001
Revises:
Create Date: 2025-04-10

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "profession",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "skill",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "warrior",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("race", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("level", sa.Integer(), nullable=False),
        sa.Column("profession_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["profession_id"],
            ["profession.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "skillwarriorlink",
        sa.Column("skill_id", sa.Integer(), nullable=False),
        sa.Column("warrior_id", sa.Integer(), nullable=False),
        sa.Column("level", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["skill_id"],
            ["skill.id"],
        ),
        sa.ForeignKeyConstraint(
            ["warrior_id"],
            ["warrior.id"],
        ),
        sa.PrimaryKeyConstraint("skill_id", "warrior_id"),
    )


def downgrade() -> None:
    op.drop_table("skillwarriorlink")
    op.drop_table("warrior")
    op.drop_table("skill")
    op.drop_table("profession")
