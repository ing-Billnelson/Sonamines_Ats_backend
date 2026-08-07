"""Port repository pour la gestion des notifications internes."""

from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from ..entities import Notification


class NotificationRepository(ABC):
    """Interface repository pour la gestion des notifications internes."""

    @abstractmethod
    async def sauvegarder(self, notification: Notification) -> Notification:
        """Sauvegarde une notification et retourne l'entité mise à jour."""
        pass

    @abstractmethod
    async def obtenir_par_id(self, notification_id: UUID) -> Optional[Notification]:
        """Récupère une notification par son ID."""
        pass

    @abstractmethod
    async def lister_par_utilisateur(
        self, utilisateur_id: UUID, limit: int = 50, offset: int = 0
    ) -> list[Notification]:
        """Liste les notifications d'un utilisateur (paginé)."""
        pass

    @abstractmethod
    async def lister_non_lues_par_utilisateur(
        self, utilisateur_id: UUID
    ) -> list[Notification]:
        """Liste les notifications non lues d'un utilisateur."""
        pass

    @abstractmethod
    async def compter_non_lues_par_utilisateur(self, utilisateur_id: UUID) -> int:
        """Compte les notifications non lues d'un utilisateur."""
        pass

    @abstractmethod
    async def marquer_toutes_comme_lues(self, utilisateur_id: UUID) -> int:
        """Marque toutes les notifications d'un utilisateur comme lues."""
        pass

    @abstractmethod
    async def supprimer_anciennes(self, jours: int = 90) -> int:
        """Supprime les notifications anciennes (par défaut > 90 jours)."""
        pass