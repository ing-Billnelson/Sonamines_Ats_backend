"""Énumération des types d'événements notifiables."""

from enum import Enum


class TypeEvenement(str, Enum):
    """Types d'événements qui peuvent déclencher des notifications."""

    # Événements de compte
    COMPTE_CREE = "COMPTE_CREE"
    COMPTE_VALIDE = "COMPTE_VALIDE"
    MOT_DE_PASSE_REINITIALISE = "MOT_DE_PASSE_REINITIALISE"

    # Événements de candidature
    CANDIDATURE_RECUE = "CANDIDATURE_RECUE"
    CANDIDATURE_DOSSIER_COMPLET = "CANDIDATURE_DOSSIER_COMPLET"
    CANDIDATURE_PRESELECTIONNEE = "CANDIDATURE_PRESELECTIONNEE"
    CANDIDATURE_CONVOQUEE = "CANDIDATURE_CONVOQUEE"
    CANDIDATURE_SELECTIONNEE = "CANDIDATURE_SELECTIONNEE"
    CANDIDATURE_REJETEE = "CANDIDATURE_REJETEE"

    # Événements d'offre
    NOUVELLE_OFFRE_PUBLIEE = "NOUVELLE_OFFRE_PUBLIEE"
    OFFRE_CLOTUREE = "OFFRE_CLOTUREE"

    def __str__(self) -> str:
        return self.value