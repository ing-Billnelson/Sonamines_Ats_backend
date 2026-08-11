"""Ajout valeurs manquantes enum statutcandidature

Revision ID: c5d8e2f4a1b9
Revises: b3f7a9c2d1e4
Create Date: 2026-08-11 10:58:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'c5d8e2f4a1b9'
down_revision: Union[str, None] = 'b3f7a9c2d1e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Note PostgreSQL :
# ALTER TYPE ... ADD VALUE est exécutable à l'intérieur d'un bloc de
# transaction depuis PostgreSQL 12. Ce projet utilise PostgreSQL 15.17
# (vérifié), donc aucune précaution spéciale (autocommit, transaction
# séparée) n'est requise : les ADD VALUE peuvent être exécutés tels quels
# dans la transaction de la migration.


def upgrade() -> None:
    """Ajoute les 8 valeurs manquantes au type ENUM statutcandidature."""
    op.execute("ALTER TYPE statutcandidature ADD VALUE 'RECUE'")
    op.execute("ALTER TYPE statutcandidature ADD VALUE 'DOSSIER_COMPLET'")
    op.execute("ALTER TYPE statutcandidature ADD VALUE 'PRESELECTIONNEE'")
    op.execute("ALTER TYPE statutcandidature ADD VALUE 'CONVOQUEE'")
    op.execute("ALTER TYPE statutcandidature ADD VALUE 'EN_ENTRETIEN'")
    op.execute("ALTER TYPE statutcandidature ADD VALUE 'SELECTIONNEE'")
    op.execute("ALTER TYPE statutcandidature ADD VALUE 'EN_ATTENTE'")
    op.execute("ALTER TYPE statutcandidature ADD VALUE 'REJETEE'")


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
        "Impossible de retirer des valeurs du type ENUM statutcandidature "
        "sans recréer entièrement le type. Downgrade non pris en charge."
    )
