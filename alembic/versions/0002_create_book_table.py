"""create book tble

Revision ID: d32ce6bdb98c
Revises: 61ebdd601d5b
Create Date: 2024-06-22 23:25:21.339884

"""
from datetime import datetime
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d32ce6bdb98c"
down_revision: Union[str, None] = "61ebdd601d5b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "book",
        sa.Column("book_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(length=32), nullable=False),
        sa.Column("division", sa.String(length=32), nullable=False),
        sa.Column("file_path", sa.String(length=128), nullable=False),
        sa.Column("file_size", sa.Integer(), nullable=False),
        sa.Column("num_chapters", sa.Integer(), nullable=False),
        sa.Column("insert_date", sa.DateTime(), nullable=False, default=datetime.utcnow),
        sa.PrimaryKeyConstraint("book_id"),
        sa.UniqueConstraint("title"),
    )


def downgrade() -> None:
    op.drop_table("book")
