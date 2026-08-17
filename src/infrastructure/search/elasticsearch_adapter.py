"""Adapter Elasticsearch pour la recherche."""

from typing import Any, Dict, List
from uuid import UUID

from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import ApiError, TransportError

from ...domain.entities import Candidature, Offre
from ...domain.exceptions import RechercheIndisponibleError
from ...domain.ports import SearchPort
from ..config import Settings
from .mappings.candidature_mapping import CANDIDATURE_MAPPING
from .mappings.offre_mapping import OFFRE_MAPPING


class ElasticsearchAdapter(SearchPort):
    """Adapter Elasticsearch pour l'indexation et la recherche."""

    def __init__(self, settings: Settings):
        self._settings = settings
        self._client = AsyncElasticsearch([settings.elasticsearch_url])
        self._index_offres = "offres"
        self._index_candidatures = "candidatures"

    async def indexer_offre(self, offre: Offre) -> bool:
        """Indexe une offre dans Elasticsearch."""
        try:
            document = self._offre_vers_document(offre)
            
            await self._client.index(
                index=self._index_offres,
                id=str(offre.id),
                body=document,
            )
            return True
        except (ApiError, TransportError):
            return False

    async def indexer_candidature(self, candidature: Candidature) -> bool:
        """Indexe une candidature dans Elasticsearch."""
        try:
            document = self._candidature_vers_document(candidature)
            
            await self._client.index(
                index=self._index_candidatures,
                id=str(candidature.id),
                body=document,
            )
            return True
        except (ApiError, TransportError):
            return False

    async def supprimer_offre_index(self, offre_id: UUID) -> bool:
        """Supprime une offre de l'index Elasticsearch."""
        try:
            await self._client.delete(
                index=self._index_offres,
                id=str(offre_id),
            )
            return True
        except (ApiError, TransportError):
            return False

    async def supprimer_candidature_index(self, candidature_id: UUID) -> bool:
        """Supprime une candidature de l'index Elasticsearch."""
        try:
            await self._client.delete(
                index=self._index_candidatures,
                id=str(candidature_id),
            )
            return True
        except (ApiError, TransportError):
            return False

    async def rechercher_offres(
        self,
        criteres: Dict[str, Any],
        limit: int = 20,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """Recherche des offres selon les critères."""
        try:
            query = self._construire_requete_offres(criteres)

            body: Dict[str, Any] = {
                "query": query,
                "size": limit,
                "from": offset,
            }
            if criteres.get("tri") == "date_creation":
                body["sort"] = [{"date_creation": {"order": "desc"}}]
            else:
                body["sort"] = [{"_score": {"order": "desc"}}]

            response = await self._client.search(
                index=self._index_offres,
                body=body,
            )

            return self._traiter_reponse_recherche(response)
        except (ApiError, TransportError) as e:
            raise RechercheIndisponibleError(str(e)) from e

    async def rechercher_candidatures(
        self,
        criteres: Dict[str, Any],
        limit: int = 20,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """Recherche des candidatures selon les critères."""
        try:
            query = self._construire_requete_candidatures(criteres)

            response = await self._client.search(
                index=self._index_candidatures,
                body={
                    "query": query,
                    "size": limit,
                    "from": offset,
                    "sort": [{"date_soumission": {"order": "desc"}}],
                }
            )

            return self._traiter_reponse_recherche(response)
        except (ApiError, TransportError) as e:
            raise RechercheIndisponibleError(str(e)) from e

    async def reinitialiser_index_offres(self) -> bool:
        """Recrée l'index des offres."""
        try:
            # Supprimer l'index s'il existe
            await self._client.indices.delete(index=self._index_offres, ignore=[404])
            
            # Créer le nouvel index avec le mapping
            mapping = self._obtenir_mapping_offres()
            await self._client.indices.create(
                index=self._index_offres,
                body={"mappings": mapping}
            )
            return True
        except (ApiError, TransportError):
            return False

    async def reinitialiser_index_candidatures(self) -> bool:
        """Recrée l'index des candidatures."""
        try:
            # Supprimer l'index s'il existe
            await self._client.indices.delete(index=self._index_candidatures, ignore=[404])
            
            # Créer le nouvel index avec le mapping
            mapping = self._obtenir_mapping_candidatures()
            await self._client.indices.create(
                index=self._index_candidatures,
                body={"mappings": mapping}
            )
            return True
        except (ApiError, TransportError):
            return False

    def _offre_vers_document(self, offre: Offre) -> Dict[str, Any]:
        """Convertit une offre en document Elasticsearch."""
        return {
            "id": str(offre.id),
            "numero_reference": str(offre.numero_reference),
            "titre": offre.titre,
            "description": offre.description,
            "type_offre": offre.type_offre.value,
            "type_contrat": offre.type_contrat.value if offre.type_contrat else None,
            "type_stage": offre.type_stage.value if offre.type_stage else None,
            "statut": offre.statut.value,
            "lieu": offre.lieu,
            "salaire_min": offre.salaire_min,
            "salaire_max": offre.salaire_max,
            "competences_requises": offre.competences_requises,
            "experience_requise": offre.experience_requise,
            "date_creation": offre.date_creation.isoformat(),
            "date_publication": offre.date_publication.isoformat() if offre.date_publication else None,
            "date_cloture": offre.date_cloture.isoformat() if offre.date_cloture else None,
            "date_limite_candidature": offre.date_limite_candidature.isoformat() if offre.date_limite_candidature else None,
        }

    def _candidature_vers_document(self, candidature: Candidature) -> Dict[str, Any]:
        """Convertit une candidature en document Elasticsearch."""
        return {
            "id": str(candidature.id),
            "numero_reference": str(candidature.numero_reference),
            "candidat_id": str(candidature.candidat_id),
            "offre_id": str(candidature.offre_id) if candidature.offre_id else None,
            "statut": candidature.statut.value,
            "message_motivation": candidature.message_motivation,
            "notes_internes": candidature.notes_internes,
            "date_soumission": candidature.date_soumission.isoformat(),
            "date_derniere_modification": candidature.date_derniere_modification.isoformat(),
            "est_spontanee": candidature.est_spontanee(),
        }

    def _construire_requete_offres(self, criteres: Dict[str, Any]) -> Dict[str, Any]:
        """Construit une requête bool Elasticsearch pour les offres."""
        must: List[Dict[str, Any]] = []
        filters: List[Dict[str, Any]] = []

        # Recherche textuelle libre : multi_match avec boost sur le titre,
        # analyseur français (défini dans le mapping).
        if criteres.get("texte"):
            must.append({
                "multi_match": {
                    "query": criteres["texte"],
                    "fields": ["titre^2", "description"],
                    "analyzer": "french",
                }
            })

        # Filtres d'égalité sur champs keyword
        if criteres.get("type_offre"):
            filters.append({"term": {"type_offre": criteres["type_offre"]}})
        if criteres.get("type_contrat"):
            filters.append({"term": {"type_contrat": criteres["type_contrat"]}})
        if criteres.get("type_stage"):
            filters.append({"term": {"type_stage": criteres["type_stage"]}})
        if criteres.get("statut"):
            filters.append({"term": {"statut": criteres["statut"]}})

        # Lieu : match insensible à la casse (champ text du mapping)
        if criteres.get("lieu"):
            filters.append({"match": {"lieu": criteres["lieu"]}})

        # Compétences : matching sur la liste (per_field: chaque compétence
        # est un keyword ; on matche au moins l'une d'elles)
        if criteres.get("competences"):
            filters.append({"terms": {"competences_requises": criteres["competences"]}})

        # Salaire : range query (chevauchant la fourchette)
        salaire_range: Dict[str, Any] = {}
        if criteres.get("salaire_min") is not None:
            salaire_range["gte"] = criteres["salaire_min"]
        if criteres.get("salaire_max") is not None:
            salaire_range["lte"] = criteres["salaire_max"]
        if salaire_range:
            filters.append({
                "bool": {
                    "should": [
                        {"range": {"salaire_min": {"lte": salaire_range.get("lte", 10**12)}}},
                        {"range": {"salaire_max": {"gte": salaire_range.get("gte", 0)}}},
                    ],
                    "minimum_should_match": 1,
                }
            })

        # Expérience requise : text — match partiel
        if criteres.get("experience_requise"):
            filters.append({"match": {"experience_requise": criteres["experience_requise"]}})

        # Dates : range query
        if criteres.get("date_limite_candidature"):
            filters.append({
                "range": {"date_limite_candidature": {"gte": criteres["date_limite_candidature"]}}
            })
        if criteres.get("date_publication"):
            filters.append({
                "range": {"date_publication": {"lte": criteres["date_publication"]}}
            })

        # Bool final : must (pertinence) + filter (filtres non scorés)
        body: Dict[str, Any] = {}
        if must:
            body["must"] = must
        if filters:
            body["filter"] = filters

        if not body:
            return {"match_all": {}}

        return {"bool": body}

    async def verifier_ou_creer_indexes(self) -> None:
        """Vérifie et crée les index Elasticsearch s'ils n'existent pas."""
        try:
            if not await self._client.indices.exists(index=self._index_offres):
                await self._client.indices.create(
                    index=self._index_offres,
                    body={"mappings": OFFRE_MAPPING},
                )
            if not await self._client.indices.exists(index=self._index_candidatures):
                await self._client.indices.create(
                    index=self._index_candidatures,
                    body={"mappings": CANDIDATURE_MAPPING},
                )
        except (ApiError, TransportError) as e:
            raise RechercheIndisponibleError(str(e)) from e

    def _construire_requete_candidatures(self, criteres: Dict[str, Any]) -> Dict[str, Any]:
        """Construit une requête Elasticsearch pour les candidatures."""
        # TODO: Implémenter la construction de requête complète
        # Requête simple pour le scaffold
        if criteres.get("texte"):
            return {
                "multi_match": {
                    "query": criteres["texte"],
                    "fields": ["numero_reference^2", "message_motivation", "notes_internes"]
                }
            }
        else:
            return {"match_all": {}}

    def _traiter_reponse_recherche(self, response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Traite la réponse d'Elasticsearch."""
        resultats = []
        for hit in response["hits"]["hits"]:
            resultat = hit["_source"]
            resultat["_score"] = hit["_score"]
            resultats.append(resultat)
        return resultats

    def _obtenir_mapping_offres(self) -> Dict[str, Any]:
        """Retourne le mapping Elasticsearch pour les offres."""
        return OFFRE_MAPPING

    def _obtenir_mapping_candidatures(self) -> Dict[str, Any]:
        """Retourne le mapping Elasticsearch pour les candidatures."""
        return CANDIDATURE_MAPPING