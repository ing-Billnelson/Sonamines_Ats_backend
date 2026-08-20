"""Énumération des disponibilités d'un candidat."""

from enum import Enum


class Disponibilite(str, Enum):
    """Disponibilités possibles d'un candidat."""

    IMMEDIATE = "IMMEDIATE"
    SOUS_PREAVIS = "SOUS_PREAVIS"
    DATE_PRECISE = "DATE_PRECISE"

    def __str__(self) -> str:
        return self.value
