"""Ajout colonnes manquantes candidatures

Revision ID: b3f7a9c2d1e4
Revises: 9e4c2a1b5d0f
Create Date: 2026-08-11 10:50:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b3f7a9c2d1e4'
down_revision: Union[str, None] = '9e4c2a1b5d0f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Ajoute les colonnes manquantes de candidatures (table vide à la création)."""
    # La table candidatures est vide (0 ligne vérifié avant rédaction) :
    # les colonnes NOT NULL peuvent être ajoutées directement, sans
    # server_default temporaire ni backfill.
    op.add_column('candidatures', sa.Column('numero_reference', sa.String(length=50), nullable=False))
    op.add_column('candidatures', sa.Column('message_motivation', sa.Text(), nullable=False))
    op.add_column('candidatures', sa.Column('notes_internes', sa.Text(), nullable=True))
    op.add_column('candidatures', sa.Column('date_soumission', sa.DateTime(), nullable=False))
    op.add_column('candidatures', sa.Column('date_derniere_modification', sa.DateTime(), nullable=False))
    op.create_index(op.f('ix_candidatures_numero_reference'), 'candidatures', ['numero_reference'], unique=True)

    # offre_id devient nullable (None = candidature spontanée)
    op.alter_column('candidatures', 'offre_id',
                    existing_type=sa.UUID(),
                    nullable=True)


def downgrade() -> None:
    """Inverse exact : suppression des colonnes et offre_id NOT NULL."""
    # Remise de offre_id en NOT NULL.
    # ATTENTION : cette opération peut échouer si des lignes possèdent
    # offre_id = NULL au moment du downgrade (contrainte violée), car des
    # candidatures spontanées peuvent avoir été créées depuis l'upgrade.
    op.alter_column('candidatures', 'offre_id',
                    existing_type=sa.UUID(),
                    nullable=False)
    op.drop_index(op.f('ix_candidatures_numero_reference'), table_name='candidatures')
    op.drop_column('candidatures', 'date_derniere_modification')
    op.drop_column('candidatures', 'date_soumission')
    op.drop_column('candidatures', 'notes_internes')
    op.drop_column('candidatures', 'message_motivation')
    op.drop_column('candidatures', 'numero_reference')
