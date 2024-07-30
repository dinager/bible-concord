"""create_phrase_table

Revision ID: 9d50950acced
Revises: 1d22bfdd393c
Create Date: 2024-07-24 17:00:41.197021

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9d50950acced"
down_revision: Union[str, None] = "1d22bfdd393c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "phrase",
        sa.Column("phrase_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("phrase_id"),
        sa.UniqueConstraint("name"),  # todo: rename to text
    )


def downgrade() -> None:
    op.drop_table("phrase")
