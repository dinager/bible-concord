"""create_words_in_group_table

Revision ID: 1d22bfdd393c
Revises: def3b1b0098b
Create Date: 2024-07-21 09:12:59.849226

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1d22bfdd393c"
down_revision: Union[str, None] = "def3b1b0098b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "word_in_group",
        sa.Column("group_id", sa.Integer(), nullable=False),
        sa.Column("word_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["group_id"], ["group.group_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["word_id"], ["word.word_id"], ondelete="CASCADE"),
        sa.UniqueConstraint("group_id", "word_id"),
    )


def downgrade() -> None:
    op.drop_table("word_in_group")
