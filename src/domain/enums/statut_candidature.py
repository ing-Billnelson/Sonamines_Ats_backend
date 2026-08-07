"""Énumération des statuts possibles d'une candidature."""

from enum import Enum


class StatutCandidature(str, Enum):
    """Statuts possibles d'une candidature dans le processus de recrutement."""

    RECUE = "RECUE"
    DOSSIER_COMPLET = "DOSSIER_COMPLET"
    PRESELECTIONNEE = "PRESELECTIONNEE"
    CONVOQUEE = "CONVOQUEE"
    EN_ENTRETIEN = "EN_ENTRETIEN"
    SELECTIONNEE = "SELECTIONNEE"
    EN_ATTENTE = "EN_ATTENTE"
    REJETEE = "REJETEE"
    RETIREE = "RETIREE"

    def __str__(self) -> str:
        return self.value

    @property
    def is_terminal(self) -> bool:
        """Vérifie si le statut est terminal (pas de transition possible)."""
        return self in {
            StatutCandidature.SELECTIONNEE,
            StatutCandidature.REJETEE,
            StatutCandidature.RETIREE,
        }

    @property
    def is_active(self) -> bool:
        """Vérifie si le statut indique une candidature active."""
        return self not in {
            StatutCandidature.REJETEE,
            StatutCandidature.RETIREE,
        }