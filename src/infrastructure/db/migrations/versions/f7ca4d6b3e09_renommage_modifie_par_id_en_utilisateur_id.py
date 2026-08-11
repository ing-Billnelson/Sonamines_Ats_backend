"""Renommage colonne modifie_par_id en utilisateur_id (historique_statuts)

Revision ID: f7ca4d6b3e09
Revises: e6b9f3c5d2a8
Create Date: 2026-08-11 11:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f7ca4d6b3e09'
down_revision: Union[str, None] = 'e6b9f3c5d2a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Renomme modifie_par_id en utilisateur_id et recrée la FK associée."""
    # 1. Supprimer l'ancienne contrainte FK (nom exact vérifié via \d historique_statuts)
    op.drop_constraint(
        'historique_statuts_modifie_par_id_fkey',
        'historique_statuts',
        type_='foreignkey',
    )

    # 2. Renommer la colonne
    op.alter_column(
        'historique_statuts',
        'modifie_par_id',
        new_column_name='utilisateur_id',
    )

    # 3. Recréer la FK sur la nouvelle colonne, vers utilisateurs.id
    op.create_foreign_key(
        'historique_statuts_utilisateur_id_fkey',
        'historique_statuts',
        'utilisateurs',
        ['utilisateur_id'],
        ['id'],
    )


def downgrade() -> None:
    """Inverse exact : recrée la colonne modifie_par_id et son ancienne FK."""
    # 1. Supprimer la FK créée à l'upgrade
    op.drop_constraint(
        'historique_statuts_utilisateur_id_fkey',
        'historique_statuts',
        type_='foreignkey',
    )

    # 2. Renommer utilisateur_id en modifie_par_id
    op.alter_column(
        'historique_statuts',
        'utilisateur_id',
        new_column_name='modifie_par_id',
    )

    # 3. Recréer l'ancienne FK avec son nom d'origine
    op.create_foreign_key(
        'historique_statuts_modifie_par_id_fkey',
        'historique_statuts',
        'utilisateurs',
        ['modifie_par_id'],
        ['id'],
    )
