"""creatw cahpter table

Revision ID: cdc18e74ff52
Revises: d32ce6bdb98c
Create Date: 2024-06-22 23:25:33.512276

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "cdc18e74ff52"
down_revision: Union[str, None] = "d32ce6bdb98c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "chapter",
        sa.Column("book_id", sa.Integer(), nullable=False),
        sa.Column("num_chapter", sa.Integer(), nullable=False),
        sa.Column("num_verses", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["book_id"], ["book.book_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("book_id", "num_chapter"),
    )


def downgrade() -> None:
    op.drop_table("chapter")
