"""Suppression colonnes obsolètes candidatures

Revision ID: e6b9f3c5d2a8
Revises: c5d8e2f4a1b9
Create Date: 2026-08-11 11:12:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e6b9f3c5d2a8'
down_revision: Union[str, None] = 'c5d8e2f4a1b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Supprime les 3 colonnes obsolètes de candidatures.

    Ces colonnes (lettre_motivation, date_candidature, date_modification)
    ne sont plus utilisées par le modèle SQLAlchemy ni par le code
    applicatif (remplacées par message_motivation, date_soumission,
    date_derniere_modification).
    """
    op.drop_column('candidatures', 'lettre_motivation')
    op.drop_column('candidatures', 'date_candidature')
    op.drop_column('candidatures', 'date_modification')


def downgrade() -> None:
    """Réajoute les colonnes avec leurs caractéristiques d'origine."""
    # Caractéristiques d'origine issues de la migration 1fbd1d88b789
    # (table candidatures) : lettre_motivation Text nullable=True,
    # date_candidature DateTime nullable=False, date_modification DateTime
    # nullable=True.
    #
    # ATTENTION : le downgrade recrée les colonnes mais ne peut PAS
    # restaurer les données qui y existaient avant l'upgrade. Elles seront
    # NULL (ou vides) après un downgrade si des lignes existent en table.
    op.add_column('candidatures', sa.Column('lettre_motivation', sa.Text(), nullable=True))
    op.add_column('candidatures', sa.Column('date_candidature', sa.DateTime(), nullable=False))
    op.add_column('candidatures', sa.Column('date_modification', sa.DateTime(), nullable=True))
