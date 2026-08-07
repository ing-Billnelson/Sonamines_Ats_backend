"""Énumérations du domaine métier."""

from .canal_notification import CanalNotification
from .categorie_fichier import CategorieFichier
from .statut_candidature import StatutCandidature
from .statut_compte import StatutCompte
from .type_contrat import TypeContrat
from .type_evenement import TypeEvenement
from .type_offre import TypeOffre
from .type_stage import TypeStage

__all__ = [
    "CanalNotification",
    "CategorieFichier",
    "StatutCandidature",
    "StatutCompte",
    "TypeContrat",
    "TypeEvenement",
    "TypeOffre",
    "TypeStage",
]