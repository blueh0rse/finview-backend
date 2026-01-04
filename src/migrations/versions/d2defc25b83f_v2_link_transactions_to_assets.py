"""v2 link transactions to assets

Revision ID: d2defc25b83f
Revises: 4ebaea01350b
Create Date: 2026-01-04 21:35:24.850599

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d2defc25b83f"
down_revision: Union[str, Sequence[str], None] = "4ebaea01350b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_foreign_key(
        "transactions_asset_symbol_fkey",
        "transactions",
        "assets",
        ["asset_symbol"],
        ["symbol"],
        ondelete="CASCADE",
    )


def downgrade():
    op.drop_constraint(
        "transactions_asset_symbol_fkey",
        "transactions",
        type_="foreignkey",
    )
