"""Rendre message motivation optionnel

Revision ID: 02052f8cc6e9
Revises: e3ae063cc463
Create Date: 2026-08-19 09:16:52.395738

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '02052f8cc6e9'
down_revision: Union[str, None] = 'e3ae063cc463'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Rend la colonne message_motivation nullable (optionnel)."""
    op.alter_column('candidatures', 'message_motivation',
               existing_type=sa.TEXT(),
               nullable=True)


def downgrade() -> None:
    """Rend la colonne message_motivation à nouveau non-nullable."""
    op.alter_column('candidatures', 'message_motivation',
               existing_type=sa.TEXT(),
               nullable=False)
