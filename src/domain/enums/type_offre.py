"""Énumération des types d'offres disponibles."""

from enum import Enum


class TypeOffre(str, Enum):
    """Types d'offres disponibles sur la plateforme."""

    EMPLOI = "EMPLOI"
    STAGE = "STAGE"

    def __str__(self) -> str:
        return self.value