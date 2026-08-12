"""Use case pour rechercher des offres."""

from uuid import UUID

from ...domain.exceptions import OffreIntrouvableError
from ...domain.ports import OffreRepository
from ..dto import OffreDTO, RechercherOffresDTO


class RechercherOffresUseCase:
    """Use case pour rechercher/lister des offres ouvertes.

    Implémentation actuelle basée uniquement sur le repository PostgreSQL
    (lister_offres_ouvertes), avec filtres simples appliqués en mémoire.
    Une recherche full-text via Elasticsearch pourra être ajoutée plus tard.
    """

    def __init__(self, offre_repository: OffreRepository):
        self._offre_repository = offre_repository

    async def executer(self, donnees: RechercherOffresDTO) -> list[OffreDTO]:
        """Recherche les offres ouvertes selon les critères (filtres simples)."""
        offres = await self._offre_repository.lister_offres_ouvertes()

        # Filtres simples appliqués en mémoire
        if donnees.type_offre is not None:
            offres = [o for o in offres if o.type_offre == donnees.type_offre]

        if donnees.lieu:
            lieu = donnees.lieu.lower()
            offres = [o for o in offres if o.lieu and lieu in o.lieu.lower()]

        if donnees.texte:
            texte = donnees.texte.lower()
            offres = [
                o
                for o in offres
                if texte in o.titre.lower() or texte in o.description.lower()
            ]

        # TODO: Filtrer sur competences / salaire_min / salaire_max — non
        # implémenté dans cette version simple basée sur le repository.

        # Pagination
        offset = donnees.offset
        limit = donnees.limit
        page_offres = offres[offset:offset + limit]

        return [self._convertir_en_dto(offre) for offre in page_offres]

    async def executer_par_id(self, offre_id: str) -> OffreDTO:
        """Récupère une offre par son ID, quelle que soit sa disponibilité."""
        offre = await self._offre_repository.obtenir_par_id(UUID(offre_id))
        if not offre:
            raise OffreIntrouvableError(offre_id)

        return self._convertir_en_dto(offre)

    def _convertir_en_dto(self, offre) -> OffreDTO:
        """Convertit une offre en DTO de sortie."""
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
            # createur_nom_complet non résolu ici (pas de repository
            # utilisateur injecté) : champ obligatoire du DTO, mis à "".
            createur_nom_complet="",
            date_creation=offre.date_creation.isoformat(),
            date_publication=(
                offre.date_publication.isoformat() if offre.date_publication else None
            ),
            date_cloture=(
                offre.date_cloture.isoformat() if offre.date_cloture else None
            ),
        )
