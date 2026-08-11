"""Ajout code de validation utilisateur

Revision ID: 838b7bc1dac4
Revises: 1fbd1d88b789
Create Date: 2026-08-10 22:05:24.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '838b7bc1dac4'
down_revision: Union[str, None] = '1fbd1d88b789'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Ajoute les colonnes de code de validation sur la table utilisateurs."""
    op.add_column('utilisateurs', sa.Column('code_validation', sa.String(), nullable=True))
    op.add_column('utilisateurs', sa.Column('code_validation_expiration', sa.DateTime(), nullable=True))


def downgrade() -> None:
    """Supprime les colonnes de code de validation de la table utilisateurs."""
    op.drop_column('utilisateurs', 'code_validation_expiration')
    op.drop_column('utilisateurs', 'code_validation')
