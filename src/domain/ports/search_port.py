"""Port pour l'indexation et la recherche avec Elasticsearch."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID

from ..entities import Candidat, Candidature, Offre


class SearchPort(ABC):
    """Interface pour l'indexation et la recherche."""

    @abstractmethod
    async def indexer_offre(self, offre: Offre) -> bool:
        """Indexe une offre dans Elasticsearch."""
        pass

    @abstractmethod
    async def indexer_candidature(
        self,
        candidature: Candidature,
        candidat: Optional[Candidat] = None,
        offre: Optional[Offre] = None,
    ) -> bool:
        """Indexe une candidature dans Elasticsearch.

        Args:
            candidature: L'entité candidature à indexer
            candidat: Entité candidat (optionnelle) pour dénormaliser les
                champs de profil (nom, email, sexe, niveau_academique, etc.)
                dans le document indexé.
            offre: Entité offre (optionnelle) pour dénormaliser les champs de
                l'offre associée (titre, lieu, type_offre, type_stage, etc.)
                dans le document indexé.
        """
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
    ) -> Tuple[List[Dict[str, Any]], int]:
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
                - sexe, niveau_academique, diplome, domaine_formation, specialite,
                  disponibilite, region_origine, region_residence: filtres keyword
                  sur les champs dénormalisés du profil candidat
                - competences, langues_parlees: filtres terms sur les champs tableau
                - age_min, age_max: filtres range sur candidat_date_naissance
                - type_offre: filtre sur offre_type_offre (EMPLOI/STAGE)
            limit: Nombre maximum de résultats
            offset: Décalage pour la pagination

        Returns:
            Tuple (liste des candidatures trouvées avec leurs données de
            pertinence, nombre total de résultats correspondant aux critères)
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