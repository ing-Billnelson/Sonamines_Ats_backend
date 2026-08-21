"""ajout_eligibilite_offre_score_candidature

Revision ID: 1c061bfd7ab4
Revises: dcc348f717fe
Create Date: 2026-08-20 21:50:20.275476

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '1c061bfd7ab4'
down_revision: Union[str, None] = 'dcc348f717fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Ajoute les critères d'éligibilité sur offres et le score sur candidatures.

    Les types ENUM niveauacademique/disponibilite existent déjà en base
    (créés par la migration d'extension du profil candidat) : aucune création
    de type nécessaire ici.
    """
    # Candidatures : score d'éligibilité (0-100), nullable
    op.add_column('candidatures', sa.Column('score_eligibilite', sa.Float(), nullable=True))

    # Offres : critères d'éligibilité pour scorer les candidatures
    # eligibilite_activee est NOT NULL sans serveur_default (default Python) :
    # on ajoute un server_default 'false' pour que l'ALTER passe même sur une
    # table déjà peuplée ; les nouvelles lignes reçoivent False par défaut.
    op.add_column('offres', sa.Column('eligibilite_activee', sa.Boolean(), nullable=False, server_default=sa.text('false')))
    op.add_column('offres', sa.Column('niveau_academique_minimum', postgresql.ENUM('BAC', 'LICENCE', 'MASTER', 'DOCTORAT', 'AUTRE', name='niveauacademique'), nullable=True))
    op.add_column('offres', sa.Column('langues_requises', sa.ARRAY(sa.String()), nullable=True))
    op.add_column('offres', sa.Column('disponibilite_requise', postgresql.ENUM('IMMEDIATE', 'SOUS_PREAVIS', 'DATE_PRECISE', name='disponibilite'), nullable=True))


def downgrade() -> None:
    """Supprime les colonnes ajoutées."""
    op.drop_column('offres', 'disponibilite_requise')
    op.drop_column('offres', 'langues_requises')
    op.drop_column('offres', 'niveau_academique_minimum')
    op.drop_column('offres', 'eligibilite_activee')
    op.drop_column('candidatures', 'score_eligibilite')

    # Le server_default 'false' de eligibilite_activee est retiré avec la
    # colonne ; les types ENUM niveauacademique/disponibilite sont laissés en
    # place (partagés avec le profil candidat).
