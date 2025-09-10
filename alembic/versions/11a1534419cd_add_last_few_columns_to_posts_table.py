"""add last few columns to posts table

Revision ID: 11a1534419cd
Revises: 2c8560da74bd
Create Date: 2025-09-09 17:54:52.467102

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "11a1534419cd"
down_revision: Union[str, Sequence[str], None] = "2c8560da74bd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean, nullable=False, server_default="TRUE"),
    )

    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(table_name="posts", column_name="published")
    op.drop_column(table_name="posts", column_name="created_at")
    pass
