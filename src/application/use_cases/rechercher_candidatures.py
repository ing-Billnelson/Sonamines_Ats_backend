"""Use case pour rechercher des candidatures (multicritère, côté RH)."""

from typing import Any, Dict

from ...domain.enums import StatutCandidature
from ...domain.ports import SearchPort
from ..dto import CandidatureDTO, RechercherCandidaturesDTO


class RechercherCandidaturesUseCase:
    """Use case pour rechercher des candidatures via Elasticsearch.

    Les critères de recherche sont convertis en une requête Elasticsearch
    (bool query). Les hits retournés par le port contiennent déjà tous les
    champs dénormalisés (profil candidat + offre), aucune requête PostgreSQL
    supplémentaire n'est nécessaire.
    """

    def __init__(self, search_port: SearchPort):
        self._search_port = search_port

    async def executer(
        self, donnees: RechercherCandidaturesDTO
    ) -> tuple[list[CandidatureDTO], int]:
        """Recherche les candidatures selon les critères.

        Returns:
            tuple[list[CandidatureDTO], int]: les candidatures de la page et
            le nombre total de résultats correspondant aux critères.
        """
        criteres = self._construire_criteres(donnees)

        hits, total = await self._search_port.rechercher_candidatures(
            criteres=criteres,
            limit=donnees.limit,
            offset=donnees.offset,
        )

        return [self._convertir_hit_en_dto(hit) for hit in hits], total

    def _construire_criteres(self, donnees: RechercherCandidaturesDTO) -> Dict[str, Any]:
        """Construit le dictionnaire de critères à destination du port de recherche."""
        criteres: Dict[str, Any] = {
            "texte": donnees.texte,
            "statut": donnees.statut.value if donnees.statut else None,
            "offre_id": donnees.offre_id,
            "candidat_nom": donnees.candidat_nom,
            "date_debut": donnees.date_debut,
            "date_fin": donnees.date_fin,
            "spontanee": donnees.spontanee,
            "sexe": donnees.sexe.value if donnees.sexe else None,
            "age_min": donnees.age_min,
            "age_max": donnees.age_max,
            "diplome": donnees.diplome,
            "domaine_formation": donnees.domaine_formation,
            "niveau_academique": (
                donnees.niveau_academique.value if donnees.niveau_academique else None
            ),
            "specialite": donnees.specialite,
            "competences": donnees.competences,
            "region_origine": donnees.region_origine,
            "region_residence": donnees.region_residence,
            "langues_parlees": donnees.langues_parlees,
            "disponibilite": (
                donnees.disponibilite.value if donnees.disponibilite else None
            ),
            "type_offre": donnees.type_offre.value if donnees.type_offre else None,
        }

        # Ne garder que les clés non vides pour éviter des filtres inutiles
        return {k: v for k, v in criteres.items() if v is not None}

    def _convertir_hit_en_dto(self, hit: Dict[str, Any]) -> CandidatureDTO:
        """Convertit un document Elasticsearch en DTO de sortie."""
        nom = hit.get("candidat_nom") or ""
        prenom = hit.get("candidat_prenom") or ""
        nom_complet = f"{prenom} {nom}".strip()

        return CandidatureDTO(
            id=str(hit["id"]),
            numero_reference=hit.get("numero_reference") or "",
            candidat_nom_complet=nom_complet,
            candidat_email=hit.get("candidat_email"),
            offre_titre=hit.get("offre_titre"),
            offre_numero_reference=None,  # non dénormalisé dans l'index
            statut=StatutCandidature(hit["statut"]),
            message_motivation=hit.get("message_motivation"),
            notes_internes=hit.get("notes_internes"),
            date_soumission=hit.get("date_soumission") or "",
            date_derniere_modification=hit.get("date_derniere_modification") or "",
            documents=[],  # TODO: Récupérer les documents réels
            historique=[],  # TODO: Récupérer l'historique réel
            est_spontanee=hit.get("est_spontanee", False),
            est_complete=False,
        )
