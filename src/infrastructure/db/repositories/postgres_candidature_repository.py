"""Repository PostgreSQL pour les candidatures."""

from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ....domain.entities import Candidature, Document, HistoriqueStatut
from ....domain.ports import CandidatureRepository
from ....domain.value_objects import NumeroReference
from ..models import CandidatureModel, DocumentModel, HistoriqueStatutModel


class PostgresCandidatureRepository(CandidatureRepository):
    """Repository PostgreSQL pour la gestion des candidatures."""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def sauvegarder(self, candidature: Candidature) -> Candidature:
        """Sauvegarde une candidature et retourne l'entité mise à jour."""
        # TODO: Implémenter la conversion entité -> modèle -> entité
        return candidature

    async def obtenir_par_id(self, candidature_id: UUID) -> Optional[Candidature]:
        """Récupère une candidature par son ID."""
        # TODO: Implémenter la récupération et conversion
        return None

    async def obtenir_par_numero_reference(
        self, numero_reference: NumeroReference
    ) -> Optional[Candidature]:
        """Récupère une candidature par son numéro de référence."""
        # TODO: Implémenter la récupération et conversion
        return None

    async def lister_par_candidat(self, candidat_id: UUID) -> list[Candidature]:
        """Liste toutes les candidatures d'un candidat."""
        # TODO: Implémenter la récupération et conversion
        return []

    async def lister_par_offre(self, offre_id: UUID) -> list[Candidature]:
        """Liste toutes les candidatures pour une offre."""
        # TODO: Implémenter la récupération et conversion
        return []

    async def lister_candidatures_spontanees(self) -> list[Candidature]:
        """Liste toutes les candidatures spontanées."""
        # TODO: Implémenter la récupération et conversion
        return []

    async def sauvegarder_document(self, document: Document) -> Document:
        """Sauvegarde un document et retourne l'entité mise à jour."""
        # TODO: Implémenter la conversion entité -> modèle -> entité
        return document

    async def obtenir_documents_candidature(
        self, candidature_id: UUID
    ) -> list[Document]:
        """Récupère tous les documents d'une candidature."""
        # TODO: Implémenter la récupération et conversion
        return []

    async def supprimer_document(self, document_id: UUID) -> bool:
        """Supprime un document du système."""
        # TODO: Implémenter la suppression
        return False

    async def sauvegarder_historique_statut(
        self, historique: HistoriqueStatut
    ) -> HistoriqueStatut:
        """Sauvegarde un historique de statut."""
        # TODO: Implémenter la conversion entité -> modèle -> entité
        return historique

    async def obtenir_historique_candidature(
        self, candidature_id: UUID
    ) -> list[HistoriqueStatut]:
        """Récupère l'historique des statuts d'une candidature."""
        # TODO: Implémenter la récupération et conversion
        return []

    async def supprimer(self, candidature_id: UUID) -> bool:
        """Supprime une candidature du système."""
        # TODO: Implémenter la suppression
        return False