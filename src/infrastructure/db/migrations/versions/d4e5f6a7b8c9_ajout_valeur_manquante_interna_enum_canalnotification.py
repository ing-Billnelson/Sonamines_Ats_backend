"""Ajout valeur manquante INTERNE enum canalnotification

Revision ID: d4e5f6a7b8c9
Revises: c3d4e5f6a7b8
Create Date: 2026-08-12 11:38:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'd4e5f6a7b8c9'
down_revision: Union[str, None] = 'c3d4e5f6a7b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Note PostgreSQL :
# ALTER TYPE ... ADD VALUE est exécutable à l'intérieur d'un bloc de
# transaction depuis PostgreSQL 12. Ce projet utilise PostgreSQL 15.17
# (vérifié), donc aucune précaution spéciale (autocommit, transaction
# séparée) n'est requise : le ADD VALUE peut être exécuté tel quel dans la
# transaction de la migration.


def upgrade() -> None:
    """Ajoute la valeur INTERNE au type ENUM canalnotification."""
    op.execute("ALTER TYPE canalnotification ADD VALUE 'INTERNE'")


def downgrade() -> None:
    """Downgrade impossible pour un ENUM PostgreSQL.

    Il est structurellement impossible de retirer (DROP VALUE) des valeurs
    d'un type ENUM PostgreSQL sans recréer entièrement le type : créer un
    nouveau type sans les valeurs à retirer, mettre à jour toutes les
    colonnes et les contraintes qui l'utilisent, puis supprimer l'ancien
    type. C'est une opération complexe et risquée (perte potentielle de
    données / échec si une valeur retirée est encore utilisée par des
    lignes existantes en base).

    Plutôt que de tenter une telle opération, on lève une erreur explicite.
    """
    raise NotImplementedError(
        "Impossible de retirer des valeurs du type ENUM canalnotification "
        "sans recréer entièrement le type. Downgrade non pris en charge."
    )
