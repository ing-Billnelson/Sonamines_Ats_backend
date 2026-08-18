"""Extension profil candidat formations experiences

Revision ID: e3ae063cc463
Revises: 0e6082dec580
Create Date: 2026-08-18 20:51:00.241745

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'e3ae063cc463'
down_revision: Union[str, None] = '0e6082dec580'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Extension du profil candidat : tables formations/experiences, nouvelles colonnes utilisateurs."""
    op.create_table('formations',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('candidat_id', sa.UUID(), nullable=False),
    sa.Column('etablissement', sa.String(length=255), nullable=False),
    sa.Column('diplome', sa.String(length=255), nullable=False),
    sa.Column('annee_debut', sa.Integer(), nullable=False),
    sa.Column('annee_fin', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['candidat_id'], ['utilisateurs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('experiences',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('candidat_id', sa.UUID(), nullable=False),
    sa.Column('entreprise', sa.String(length=255), nullable=False),
    sa.Column('poste', sa.String(length=255), nullable=False),
    sa.Column('date_debut', sa.DateTime(), nullable=False),
    sa.Column('date_fin', sa.DateTime(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['candidat_id'], ['utilisateurs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('utilisateurs', sa.Column('linkedin_url', sa.String(length=500), nullable=True))
    op.add_column('utilisateurs', sa.Column('adresse', sa.String(length=500), nullable=True))
    op.add_column('utilisateurs', sa.Column('competences', sa.ARRAY(sa.String()), nullable=True))


def downgrade() -> None:
    """Annule l'extension du profil candidat."""
    op.drop_column('utilisateurs', 'competences')
    op.drop_column('utilisateurs', 'adresse')
    op.drop_column('utilisateurs', 'linkedin_url')
    op.drop_table('experiences')
    op.drop_table('formations')
