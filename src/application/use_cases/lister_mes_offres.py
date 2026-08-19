"""Use case pour lister les offres créées par un admin RH."""

from uuid import UUID

from ...domain.ports import OffreRepository, UtilisateurRepository
from ..dto import OffreDTO


class ListerMesOffresUseCase:
    """Use case pour lister les offres créées par un admin RH."""

    def __init__(
        self,
        offre_repository: OffreRepository,
        utilisateur_repository: UtilisateurRepository,
    ):
        self._offre_repository = offre_repository
        self._utilisateur_repository = utilisateur_repository

    async def executer(self, createur_id: str) -> list[OffreDTO]:
        """Liste les offres créées par le créateur donné.

        Toutes les offres appartiennent au même créateur, on résout donc le
        nom complet une seule fois et on le partage entre les offres.
        """
        createur_uuid = UUID(createur_id)

        offres = await self._offre_repository.lister_offres_par_createur(createur_uuid)

        createur = await self._utilisateur_repository.obtenir_par_id(createur_uuid)
        createur_nom_complet = createur.nom_complet if createur else ""

        return [
            self._convertir_en_dto(offre, createur_nom_complet) for offre in offres
        ]

    def _convertir_en_dto(self, offre, createur_nom_complet: str) -> OffreDTO:
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
            createur_nom_complet=createur_nom_complet,
            date_creation=offre.date_creation.isoformat(),
            date_publication=(
                offre.date_publication.isoformat() if offre.date_publication else None
            ),
            date_cloture=(
                offre.date_cloture.isoformat() if offre.date_cloture else None
            ),
        )
