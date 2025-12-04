"""link asset to transaction

Revision ID: a4d8d81167ab
Revises: 9d51aac2e31a
Create Date: 2025-12-04 21:32:51.255730

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4d8d81167ab'
down_revision: Union[str, Sequence[str], None] = '9d51aac2e31a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_foreign_key(
        'fk_transactions_assets', 
        'transactions', 
        'assets', 
        ['asset_symbol'], 
        ['symbol'], 
        ondelete='CASCADE'
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('fk_transactions_assets', 'transactions', type_='foreignkey')