"""create word_apperance table

Revision ID: 394e6b0a33d0
Revises: 6a0c99f6de2d
Create Date: 2024-06-22 23:25:48.507179

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "394e6b0a33d0"
down_revision: Union[str, None] = "6a0c99f6de2d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "word_appearance",
        sa.Column("index", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("book_id", sa.Integer(), nullable=False),
        sa.Column("word_id", sa.Integer(), nullable=False),
        sa.Column("verse_num", sa.Integer(), nullable=False),
        sa.Column("chapter_num", sa.Integer(), nullable=False),
        sa.Column("word_position", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["book_id"], ["book.book_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["word_id"], ["word.word_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("index"),
        sa.UniqueConstraint("book_id", "word_id", "verse_num", "chapter_num", "word_position"),
    )

    op.create_index("word_appearance_word_id_idx", "word_appearance", ["word_id"])
    op.create_index("word_appearance_book_id_idx", "word_appearance", ["book_id"])


def downgrade() -> None:
    op.drop_index("idx_word_appearance", table_name="word_appearance")
    op.drop_table("word_appearance")
