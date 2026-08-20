"""extension_profil_candidat_recherche_multicritere

Revision ID: dcc348f717fe
Revises: d8ea8e4818d4
Create Date: 2026-08-20 12:36:19.971439

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'dcc348f717fe'
down_revision: Union[str, None] = 'd8ea8e4818d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Étend le profil candidat pour la recherche multicritère.

    Ajoute 10 colonnes optionnelles sur utilisateurs (profil candidat) et les
    3 types ENUM PostgreSQL correspondants. Toutes les colonnes sont NULLABLE :
    aucune donnée existante à migrer.
    """
    # Les types ENUM sexe/disponibilite/niveauacademique n'existent pas encore
    # en base : on les crée avant d'ajouter les colonnes qui les référencent.
    op.execute("CREATE TYPE sexe AS ENUM ('MASCULIN', 'FEMININ')")
    op.execute(
        "CREATE TYPE disponibilite AS ENUM ('IMMEDIATE', 'SOUS_PREAVIS', 'DATE_PRECISE')"
    )
    op.execute(
        "CREATE TYPE niveauacademique AS ENUM "
        "('BAC', 'LICENCE', 'MASTER', 'DOCTORAT', 'AUTRE')"
    )

    op.add_column('utilisateurs', sa.Column('sexe', postgresql.ENUM(name='sexe'), nullable=True))
    op.add_column('utilisateurs', sa.Column('date_naissance', sa.DateTime(), nullable=True))
    op.add_column('utilisateurs', sa.Column('nationalite', sa.String(length=100), nullable=True))
    op.add_column('utilisateurs', sa.Column('region_origine', sa.String(length=100), nullable=True))
    op.add_column('utilisateurs', sa.Column('region_residence', sa.String(length=100), nullable=True))
    op.add_column('utilisateurs', sa.Column('langues_parlees', sa.ARRAY(sa.String()), nullable=True))
    op.add_column('utilisateurs', sa.Column('disponibilite', postgresql.ENUM(name='disponibilite'), nullable=True))
    op.add_column('utilisateurs', sa.Column('niveau_academique', postgresql.ENUM(name='niveauacademique'), nullable=True))
    op.add_column('utilisateurs', sa.Column('domaine_formation', sa.String(length=255), nullable=True))
    op.add_column('utilisateurs', sa.Column('specialite', sa.String(length=255), nullable=True))


def downgrade() -> None:
    """Supprime les colonnes ajoutées pour la recherche multicritère."""
    op.drop_column('utilisateurs', 'specialite')
    op.drop_column('utilisateurs', 'domaine_formation')
    op.drop_column('utilisateurs', 'niveau_academique')
    op.drop_column('utilisateurs', 'disponibilite')
    op.drop_column('utilisateurs', 'langues_parlees')
    op.drop_column('utilisateurs', 'region_residence')
    op.drop_column('utilisateurs', 'region_origine')
    op.drop_column('utilisateurs', 'nationalite')
    op.drop_column('utilisateurs', 'date_naissance')
    op.drop_column('utilisateurs', 'sexe')

    # Les types ENUM sexe/disponibilite/niveauacademique sont laissés en
    # place (leur suppression est facultative et sans effet puisque les
    # colonnes sont retirées ; on évite un DROP TYPE potentiellement risqué).
