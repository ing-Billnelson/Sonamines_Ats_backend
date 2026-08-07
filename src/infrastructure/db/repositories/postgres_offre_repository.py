"""Repository PostgreSQL pour les offres."""

from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ....domain.entities import Offre
from ....domain.ports import OffreRepository
from ....domain.value_objects import NumeroReference
from ..models import OffreModel


class PostgresOffreRepository(OffreRepository):
    """Repository PostgreSQL pour la gestion des offres."""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def sauvegarder(self, offre: Offre) -> Offre:
        """Sauvegarde une offre et retourne l'entité mise à jour."""
        # TODO: Implémenter la conversion entité -> modèle -> entité
        return offre

    async def obtenir_par_id(self, offre_id: UUID) -> Optional[Offre]:
        """Récupère une offre par son ID."""
        # TODO: Implémenter la récupération et conversion
        return None

    async def obtenir_par_numero_reference(
        self, numero_reference: NumeroReference
    ) -> Optional[Offre]:
        """Récupère une offre par son numéro de référence."""
        # TODO: Implémenter la récupération et conversion
        return None

    async def lister_offres_ouvertes(self) -> list[Offre]:
        """Liste toutes les offres ouvertes aux candidatures."""
        # TODO: Implémenter la récupération et conversion
        return []

    async def lister_offres_par_createur(self, createur_id: UUID) -> list[Offre]:
        """Liste toutes les offres créées par un administrateur RH."""
        # TODO: Implémenter la récupération et conversion
        return []

    async def supprimer(self, offre_id: UUID) -> bool:
        """Supprime une offre du système."""
        # TODO: Implémenter la suppression
        return False