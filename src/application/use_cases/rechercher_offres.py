"""Use case pour rechercher des offres."""

from typing import Any, Dict
from uuid import UUID

from ...domain.entities.offre import StatutOffre
from ...domain.enums import TypeContrat, TypeOffre, TypeStage
from ...domain.exceptions import OffreIntrouvableError
from ...domain.ports import OffreRepository, SearchPort
from ..dto import OffreDTO, RechercherOffresDTO


class RechercherOffresUseCase:
    """Use case pour rechercher des offres via le moteur de recherche.

    La recherche multicritère est déléguée au port de recherche
    (Elasticsearch). Le repository PostgreSQL est conservé pour la
    récupération d'une offre par ID (executer_par_id). Une indisponibilité
    du moteur de recherche se propage en RechercheIndisponibleError (503).
    """

    def __init__(
        self,
        search_port: SearchPort,
        offre_repository: OffreRepository,
    ):
        self._search_port = search_port
        self._offre_repository = offre_repository

    async def executer(self, donnees: RechercherOffresDTO) -> list[OffreDTO]:
        """Recherche les offres selon les critères (via Elasticsearch)."""
        criteres = self._construire_criteres(donnees)

        hits = await self._search_port.rechercher_offres(
            criteres=criteres,
            limit=donnees.limit,
            offset=donnees.offset,
        )

        return [self._convertir_hit_en_dto(hit) for hit in hits]

    async def executer_par_id(self, offre_id: str) -> OffreDTO:
        """Récupère une offre par son ID, quelle que soit sa disponibilité."""
        offre = await self._offre_repository.obtenir_par_id(UUID(offre_id))
        if not offre:
            raise OffreIntrouvableError(offre_id)

        return self._convertir_en_dto(offre)

    def _construire_criteres(self, donnees: RechercherOffresDTO) -> Dict[str, Any]:
        """Construit le dictionnaire de critères à destination du port de recherche."""
        criteres: Dict[str, Any] = {
            "texte": donnees.texte,
            "statut": StatutOffre.OUVERTE.value,
            "type_offre": donnees.type_offre.value if donnees.type_offre else None,
            "type_contrat": donnees.type_contrat.value if donnees.type_contrat else None,
            "type_stage": donnees.type_stage.value if donnees.type_stage else None,
            "lieu": donnees.lieu,
            "competences": donnees.competences,
            "salaire_min": donnees.salaire_min,
            "salaire_max": donnees.salaire_max,
        }

        # Ne garder que les clés non vides pour éviter des filtres inutiles
        return {k: v for k, v in criteres.items() if v is not None}

    def _convertir_hit_en_dto(self, hit: Dict[str, Any]) -> OffreDTO:
        """Convertit un document Elasticsearch en DTO de sortie."""
        competences = hit.get("competences_requises") or []

        return OffreDTO(
            id=str(hit["id"]),
            numero_reference=hit.get("numero_reference"),
            titre=hit.get("titre") or "",
            description=hit.get("description") or "",
            type_offre=TypeOffre(hit["type_offre"]) if hit.get("type_offre") else None,
            type_contrat=TypeContrat(hit["type_contrat"]) if hit.get("type_contrat") else None,
            type_stage=TypeStage(hit["type_stage"]) if hit.get("type_stage") else None,
            statut=StatutOffre(hit["statut"]) if hit.get("statut") else None,
            date_limite_candidature=hit.get("date_limite_candidature"),
            lieu=hit.get("lieu") or "",
            salaire_min=hit.get("salaire_min"),
            salaire_max=hit.get("salaire_max"),
            competences_requises=competences,
            experience_requise=hit.get("experience_requise"),
            createur_nom_complet="",
            date_creation=hit.get("date_creation") or "",
            date_publication=hit.get("date_publication"),
            date_cloture=hit.get("date_cloture"),
        )

    def _convertir_en_dto(self, offre) -> OffreDTO:
        """Convertit une entité Offre en DTO de sortie (pour executer_par_id)."""
        return OffreDTO(
            id=str(offre.id),
            numero_reference=str(offre.numero_reference),
            titre=offre.titre,
            description=offre.description,
            type_offre=offre.type_offre,
            type_contrat=offre.type_contrat,
            type_stage=offre.type_stage,
            statut=offre.statut,
            date_limite_candidature=(
                offre.date_limite_candidature.isoformat()
                if offre.date_limite_candidature
                else None
            ),
            lieu=offre.lieu,
            salaire_min=offre.salaire_min,
            salaire_max=offre.salaire_max,
            competences_requises=offre.competences_requises,
            experience_requise=offre.experience_requise,
            createur_nom_complet="",
            date_creation=offre.date_creation.isoformat(),
            date_publication=(
                offre.date_publication.isoformat() if offre.date_publication else None
            ),
            date_cloture=(
                offre.date_cloture.isoformat() if offre.date_cloture else None
            ),
        )
