"""Énumération des types de contrats pour les emplois."""

from enum import Enum


class TypeContrat(str, Enum):
    """Types de contrats disponibles pour les offres d'emploi."""

    CDI = "CDI"
    CDD = "CDD"

    def __str__(self) -> str:
        return self.value