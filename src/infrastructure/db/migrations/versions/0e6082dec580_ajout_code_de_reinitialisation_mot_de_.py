"""Ajout code de reinitialisation mot de passe

Revision ID: 0e6082dec580
Revises: d4e5f6a7b8c9
Create Date: 2026-08-17 12:43:37.796698

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '0e6082dec580'
down_revision: Union[str, None] = 'd4e5f6a7b8c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Ajoute les colonnes de code de réinitialisation du mot de passe sur la table utilisateurs."""
    op.add_column('utilisateurs', sa.Column('code_reinitialisation', sa.String(), nullable=True))
    op.add_column('utilisateurs', sa.Column('code_reinitialisation_expiration', sa.DateTime(), nullable=True))


def downgrade() -> None:
    """Supprime les colonnes de code de réinitialisation du mot de passe de la table utilisateurs."""
    op.drop_column('utilisateurs', 'code_reinitialisation_expiration')
    op.drop_column('utilisateurs', 'code_reinitialisation')
