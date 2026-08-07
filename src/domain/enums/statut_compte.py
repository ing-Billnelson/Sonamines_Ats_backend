"""Énumération des statuts de comptes utilisateur."""

from enum import Enum


class StatutCompte(str, Enum):
    """Statuts possibles d'un compte utilisateur."""

    EN_ATTENTE_VALIDATION = "EN_ATTENTE_VALIDATION"
    ACTIF = "ACTIF"
    SUSPENDU = "SUSPENDU"
    DESACTIVE = "DESACTIVE"

    def __str__(self) -> str:
        return self.value

    @property
    def is_active(self) -> bool:
        """Vérifie si le compte est actif et peut se connecter."""
        return self == StatutCompte.ACTIF