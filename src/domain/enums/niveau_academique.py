"""Énumération des niveaux académiques d'un candidat."""

from enum import Enum


class NiveauAcademique(str, Enum):
    """Niveaux académiques possibles d'un candidat."""

    BAC = "BAC"
    LICENCE = "LICENCE"
    MASTER = "MASTER"
    DOCTORAT = "DOCTORAT"
    AUTRE = "AUTRE"

    def __str__(self) -> str:
        return self.value
