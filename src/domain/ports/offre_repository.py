"""Port repository pour la gestion des offres."""

from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from ..entities import Offre
from ..value_objects import NumeroReference


class OffreRepository(ABC):
    """Interface repository pour la gestion des offres."""

    @abstractmethod
    async def sauvegarder(self, offre: Offre) -> Offre:
        """Sauvegarde une offre et retourne l'entité mise à jour."""
        pass

    @abstractmethod
    async def obtenir_par_id(self, offre_id: UUID) -> Optional[Offre]:
        """Récupère une offre par son ID."""
        pass

    @abstractmethod
    async def obtenir_par_numero_reference(
        self, numero_reference: NumeroReference
    ) -> Optional[Offre]:
        """Récupère une offre par son numéro de référence."""
        pass

    @abstractmethod
    async def lister_offres_ouvertes(self) -> list[Offre]:
        """Liste toutes les offres ouvertes aux candidatures."""
        pass

    @abstractmethod
    async def lister_offres_par_createur(self, createur_id: UUID) -> list[Offre]:
        """Liste toutes les offres créées par un administrateur RH."""
        pass

    @abstractmethod
    async def supprimer(self, offre_id: UUID) -> bool:
        """Supprime une offre du système."""
        pass