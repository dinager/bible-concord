"""create group table

Revision ID: def3b1b0098b
Revises: 394e6b0a33d0
Create Date: 2024-07-21 09:04:38.491601

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "def3b1b0098b"
down_revision: Union[str, None] = "394e6b0a33d0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "group",
        sa.Column("group_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=32), nullable=False),
        sa.PrimaryKeyConstraint("group_id"),
        sa.UniqueConstraint("name"),
    )


def downgrade() -> None:
    op.drop_table("group")
