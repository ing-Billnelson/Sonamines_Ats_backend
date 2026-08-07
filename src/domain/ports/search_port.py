"""Port pour l'indexation et la recherche avec Elasticsearch."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List
from uuid import UUID

from ..entities import Candidature, Offre


class SearchPort(ABC):
    """Interface pour l'indexation et la recherche."""

    @abstractmethod
    async def indexer_offre(self, offre: Offre) -> bool:
        """Indexe une offre dans Elasticsearch."""
        pass

    @abstractmethod
    async def indexer_candidature(self, candidature: Candidature) -> bool:
        """Indexe une candidature dans Elasticsearch."""
        pass

    @abstractmethod
    async def supprimer_offre_index(self, offre_id: UUID) -> bool:
        """Supprime une offre de l'index Elasticsearch."""
        pass

    @abstractmethod
    async def supprimer_candidature_index(self, candidature_id: UUID) -> bool:
        """Supprime une candidature de l'index Elasticsearch."""
        pass

    @abstractmethod
    async def rechercher_offres(
        self,
        criteres: Dict[str, Any],
        limit: int = 20,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """
        Recherche des offres selon les critères spécifiés.

        Args:
            criteres: Dictionnaire des critères de recherche
                - texte: recherche textuelle libre
                - type_offre: EMPLOI ou STAGE
                - type_contrat: CDI ou CDD (pour les emplois)
                - type_stage: ACADEMIQUE ou PROFESSIONNEL (pour les stages)
                - lieu: localisation
                - competences: liste des compétences recherchées
                - salaire_min: salaire minimum
                - salaire_max: salaire maximum
            limit: Nombre maximum de résultats
            offset: Décalage pour la pagination

        Returns:
            Liste des offres trouvées avec leurs données de pertinence
        """
        pass

    @abstractmethod
    async def rechercher_candidatures(
        self,
        criteres: Dict[str, Any],
        limit: int = 20,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """
        Recherche des candidatures selon les critères spécifiés.

        Args:
            criteres: Dictionnaire des critères de recherche
                - texte: recherche textuelle libre
                - statut: statut de la candidature
                - offre_id: ID de l'offre (pour filtrer les candidatures d'une offre)
                - candidat_nom: nom du candidat
                - date_debut: date de début de période
                - date_fin: date de fin de période
                - spontanee: True pour les candidatures spontanées uniquement
            limit: Nombre maximum de résultats
            offset: Décalage pour la pagination

        Returns:
            Liste des candidatures trouvées avec leurs données de pertinence
        """
        pass

    @abstractmethod
    async def reinitialiser_index_offres(self) -> bool:
        """Recrée l'index des offres à partir de zéro."""
        pass

    @abstractmethod
    async def reinitialiser_index_candidatures(self) -> bool:
        """Recrée l'index des candidatures à partir de zéro."""
        pass