"""Port repository pour la gestion des candidatures."""

from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from ..entities import Candidature, Document, HistoriqueStatut
from ..enums import StatutCandidature
from ..value_objects import NumeroReference


class CandidatureRepository(ABC):
    """Interface repository pour la gestion des candidatures."""

    @abstractmethod
    async def sauvegarder(self, candidature: Candidature) -> Candidature:
        """Sauvegarde une candidature et retourne l'entité mise à jour."""
        pass

    @abstractmethod
    async def obtenir_par_id(self, candidature_id: UUID) -> Optional[Candidature]:
        """Récupère une candidature par son ID."""
        pass

    @abstractmethod
    async def obtenir_par_numero_reference(
        self, numero_reference: NumeroReference
    ) -> Optional[Candidature]:
        """Récupère une candidature par son numéro de référence."""
        pass

    @abstractmethod
    async def lister_par_candidat(self, candidat_id: UUID) -> list[Candidature]:
        """Liste toutes les candidatures d'un candidat."""
        pass

    @abstractmethod
    async def lister_par_offre(self, offre_id: UUID) -> list[Candidature]:
        """Liste toutes les candidatures pour une offre."""
        pass

    @abstractmethod
    async def lister_candidatures_spontanees(self) -> list[Candidature]:
        """Liste toutes les candidatures spontanées."""
        pass

    @abstractmethod
    async def lister_toutes(
        self,
        statut: Optional[StatutCandidature] = None,
        offre_id: Optional[UUID] = None,
        spontanee: Optional[bool] = None,
        page: int = 1,
        taille_page: int = 20,
    ) -> tuple[list[Candidature], int]:
        """Liste les candidatures avec filtres optionnels et pagination.

        Retourne un tuple (liste des candidatures de la page, nombre total
        de candidatures correspondant aux filtres).
        """
        pass

    @abstractmethod
    async def sauvegarder_document(self, document: Document) -> Document:
        """Sauvegarde un document et retourne l'entité mise à jour."""
        pass

    @abstractmethod
    async def obtenir_documents_candidature(
        self, candidature_id: UUID
    ) -> list[Document]:
        """Récupère tous les documents d'une candidature."""
        pass

    @abstractmethod
    async def supprimer_document(self, document_id: UUID) -> bool:
        """Supprime un document du système."""
        pass

    @abstractmethod
    async def sauvegarder_historique_statut(
        self, historique: HistoriqueStatut
    ) -> HistoriqueStatut:
        """Sauvegarde un historique de statut."""
        pass

    @abstractmethod
    async def obtenir_historique_candidature(
        self, candidature_id: UUID
    ) -> list[HistoriqueStatut]:
        """Récupère l'historique des statuts d'une candidature."""
        pass

    @abstractmethod
    async def supprimer(self, candidature_id: UUID) -> bool:
        """Supprime une candidature du système."""
        pass