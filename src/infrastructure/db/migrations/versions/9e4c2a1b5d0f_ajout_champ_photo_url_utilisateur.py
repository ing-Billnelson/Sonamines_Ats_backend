"""Ajout champ photo_url utilisateur

Revision ID: 9e4c2a1b5d0f
Revises: 838b7bc1dac4
Create Date: 2026-08-10 22:28:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '9e4c2a1b5d0f'
down_revision: Union[str, None] = '838b7bc1dac4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Ajoute la colonne photo_url sur la table utilisateurs."""
    op.add_column('utilisateurs', sa.Column('photo_url', sa.String(length=500), nullable=True))


def downgrade() -> None:
    """Supprime la colonne photo_url de la table utilisateurs."""
    op.drop_column('utilisateurs', 'photo_url')
