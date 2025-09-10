"""add content column to post table

Revision ID: 6f7153de4bd5
Revises: 081784ac3840
Create Date: 2025-09-09 17:37:26.422929

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6f7153de4bd5"
down_revision: Union[str, Sequence[str], None] = "081784ac3840"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "posts",
        sa.Column("content", sa.String, nullable=False),
    )
    # pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "content")
