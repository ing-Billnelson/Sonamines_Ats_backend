"""Ajout valeurs manquantes enum statutoffre

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-08-12 09:35:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'b2c3d4e5f6a7'
down_revision: Union[str, None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Note PostgreSQL :
# ALTER TYPE ... ADD VALUE est exécutable à l'intérieur d'un bloc de
# transaction depuis PostgreSQL 12. Ce projet utilise PostgreSQL 15.17
# (vérifié), donc aucune précaution spéciale (autocommit, transaction
# séparée) n'est requise : les ADD VALUE peuvent être exécutés tels quels
# dans la transaction de la migration.


def upgrade() -> None:
    """Ajoute les 3 valeurs manquantes au type ENUM statutoffre."""
    op.execute("ALTER TYPE statutoffre ADD VALUE 'OUVERTE'")
    op.execute("ALTER TYPE statutoffre ADD VALUE 'CLOTUREE'")
    op.execute("ALTER TYPE statutoffre ADD VALUE 'ARCHIVEE'")


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
        "Impossible de retirer des valeurs du type ENUM statutoffre "
        "sans recréer entièrement le type. Downgrade non pris en charge."
    )
