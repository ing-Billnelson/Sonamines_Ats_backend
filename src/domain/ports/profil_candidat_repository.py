"""Port repository pour le profil candidat (formations et expériences)."""

from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from ..entities import Experience, Formation


class ProfilCandidatRepository(ABC):
    """Interface repository pour les données de profil candidat."""

    @abstractmethod
    async def sauvegarder_formation(self, formation: Formation) -> Formation:
        """Sauvegarde une formation et retourne l'entité mise à jour."""
        pass

    @abstractmethod
    async def obtenir_formations_candidat(self, candidat_id: UUID) -> list[Formation]:
        """Récupère les formations d'un candidat."""
        pass

    @abstractmethod
    async def supprimer_formation(self, formation_id: UUID) -> bool:
        """Supprime une formation. Retourne False si absent."""
        pass

    @abstractmethod
    async def sauvegarder_experience(self, experience: Experience) -> Experience:
        """Sauvegarde une expérience et retourne l'entité mise à jour."""
        pass

    @abstractmethod
    async def obtenir_experiences_candidat(self, candidat_id: UUID) -> list[Experience]:
        """Récupère les expériences d'un candidat."""
        pass

    @abstractmethod
    async def supprimer_experience(self, experience_id: UUID) -> bool:
        """Supprime une expérience. Retourne False si absent."""
        pass
