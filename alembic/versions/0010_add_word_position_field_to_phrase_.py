"""Add_word_position_field_to_phrase_reference_table

Revision ID: b811d679ac14
Revises: f6d400849026
Create Date: 2024-07-28 00:38:09.730755

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b811d679ac14"
down_revision: Union[str, None] = "f6d400849026"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add the new column
    op.add_column("phrase_reference", sa.Column("word_position", sa.Integer, nullable=True))


def downgrade() -> None:
    # Remove the new column
    op.drop_column("phrase_reference", "word_position")
