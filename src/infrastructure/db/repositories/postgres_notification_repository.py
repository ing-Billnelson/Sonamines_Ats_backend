"""Repository PostgreSQL pour les notifications."""

from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ....domain.entities import Notification
from ....domain.ports import NotificationRepository
from ..models import NotificationModel


class PostgresNotificationRepository(NotificationRepository):
    """Repository PostgreSQL pour la gestion des notifications internes."""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def sauvegarder(self, notification: Notification) -> Notification:
        """Sauvegarde une notification et retourne l'entité mise à jour."""
        # TODO: Implémenter la conversion entité -> modèle -> entité
        return notification

    async def obtenir_par_id(self, notification_id: UUID) -> Optional[Notification]:
        """Récupère une notification par son ID."""
        # TODO: Implémenter la récupération et conversion
        return None

    async def lister_par_utilisateur(
        self, utilisateur_id: UUID, limit: int = 50, offset: int = 0
    ) -> list[Notification]:
        """Liste les notifications d'un utilisateur (paginé)."""
        # TODO: Implémenter la récupération et conversion
        return []

    async def lister_non_lues_par_utilisateur(
        self, utilisateur_id: UUID
    ) -> list[Notification]:
        """Liste les notifications non lues d'un utilisateur."""
        # TODO: Implémenter la récupération et conversion
        return []

    async def compter_non_lues_par_utilisateur(self, utilisateur_id: UUID) -> int:
        """Compte les notifications non lues d'un utilisateur."""
        # TODO: Implémenter le comptage
        return 0

    async def marquer_toutes_comme_lues(self, utilisateur_id: UUID) -> int:
        """Marque toutes les notifications d'un utilisateur comme lues."""
        # TODO: Implémenter la mise à jour en lot
        return 0

    async def supprimer_anciennes(self, jours: int = 90) -> int:
        """Supprime les notifications anciennes (par défaut > 90 jours)."""
        # TODO: Implémenter la suppression en lot
        return 0