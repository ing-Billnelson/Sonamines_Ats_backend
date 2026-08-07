"""Énumération des types de stages disponibles."""

from enum import Enum


class TypeStage(str, Enum):
    """Types de stages disponibles sur la plateforme."""

    ACADEMIQUE = "ACADEMIQUE"
    PROFESSIONNEL = "PROFESSIONNEL"

    def __str__(self) -> str:
        return self.value