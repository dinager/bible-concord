"""create phrase_reference table

Revision ID: b811d679ac14
Revises: 9d50950acced
Create Date: 2024-07-24 17:04:03.528349

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b811d679ac14"
down_revision: Union[str, None] = "9d50950acced"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "phrase_reference",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column(
            "phrase_id", sa.Integer, sa.ForeignKey("phrase.phrase_id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column("book_id", sa.Integer, nullable=False),
        sa.Column("verse_num", sa.Integer, nullable=False),
        sa.Column("chapter_num", sa.Integer, nullable=False),
        sa.Column("line_num_in_file", sa.Integer, nullable=False),
        sa.Column("word_position", sa.Integer, nullable=True),
        sa.ForeignKeyConstraint(
            ["book_id", "line_num_in_file", "verse_num", "chapter_num"],
            [
                "word_appearance.book_id",
                "word_appearance.line_num_in_file",
                "word_appearance.verse_num",
                "word_appearance.chapter_num",
            ],
            ondelete="CASCADE",
        ),
    )


def downgrade() -> None:
    op.drop_table("phrase_reference")
