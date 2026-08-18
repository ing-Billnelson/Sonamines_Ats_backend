"""Repositories PostgreSQL de l'infrastructure."""

from .postgres_candidature_repository import PostgresCandidatureRepository
from .postgres_notification_repository import PostgresNotificationRepository
from .postgres_offre_repository import PostgresOffreRepository
from .postgres_profil_candidat_repository import PostgresProfilCandidatRepository
from .postgres_utilisateur_repository import PostgresUtilisateurRepository

__all__ = [
    "PostgresCandidatureRepository",
    "PostgresNotificationRepository",
    "PostgresOffreRepository",
    "PostgresProfilCandidatRepository",
    "PostgresUtilisateurRepository",
]