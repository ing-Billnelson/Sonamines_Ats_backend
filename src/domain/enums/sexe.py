"""Énumération des sexes d'un candidat."""

from enum import Enum


class Sexe(str, Enum):
    """Sexes possibles d'un candidat."""

    MASCULIN = "MASCULIN"
    FEMININ = "FEMININ"

    def __str__(self) -> str:
        return self.value
