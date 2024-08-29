"""creatw word table

Revision ID: 6a0c99f6de2d
Revises: cdc18e74ff52
Create Date: 2024-06-22 23:25:39.509152

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6a0c99f6de2d"
down_revision: Union[str, None] = "cdc18e74ff52"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "word",
        sa.Column("word_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("value", sa.String(length=50), nullable=False),
        sa.Column("length", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("word_id"),
        sa.UniqueConstraint("value"),
    )
    op.create_index("word_value_idx", "word", ["value", "word_id"])


def downgrade() -> None:
    op.drop_table("word")
    op.drop_index("word_value_idx", table_name="word")
