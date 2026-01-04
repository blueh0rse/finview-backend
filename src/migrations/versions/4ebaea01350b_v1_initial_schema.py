"""v1 initial schema

Revision ID: 4ebaea01350b
Revises:
Create Date: 2026-01-04 21:31:59.101047

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4ebaea01350b"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "assets",
        sa.Column("symbol", sa.String(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("category", sa.String(), nullable=False),
        sa.Column("current_price", sa.Float(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
    )

    op.create_table(
        "transactions",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column("asset_symbol", sa.String(), nullable=False),
        sa.Column("operation", sa.String(), nullable=False),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("quantity", sa.Float(), nullable=False),
        sa.Column("unit_price", sa.Float(), nullable=False),
        sa.Column("currency", sa.String(), nullable=False),
        sa.Column("date", sa.DateTime(), nullable=True),
        sa.Column("comment", sa.String(), nullable=True),
    )


def downgrade():
    op.drop_table("transactions")
    op.drop_table("assets")
