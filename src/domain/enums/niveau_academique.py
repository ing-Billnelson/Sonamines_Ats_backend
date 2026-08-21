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


_ORDRE_NIVEAU: dict[NiveauAcademique, int] = {
    NiveauAcademique.BAC: 1,
    NiveauAcademique.LICENCE: 2,
    NiveauAcademique.MASTER: 3,
    NiveauAcademique.DOCTORAT: 4,
    NiveauAcademique.AUTRE: 0,
}


def ordre_niveau_academique(niveau: NiveauAcademique) -> int:
    """Retourne un ordre numérique pour comparer les niveaux académiques.

    BAC=1, LICENCE=2, MASTER=3, DOCTORAT=4, AUTRE=0 (non déterminé).
    Un AUTRE renvoie 0, ce qui échoue toute comparaison de minimum
    (un minimum > 0 ne peut être satisfait par un AUTRE).
    """
    return _ORDRE_NIVEAU[niveau]
