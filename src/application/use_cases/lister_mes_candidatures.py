"""Use case pour lister les candidatures d'un candidat."""

from uuid import UUID

from ...domain.entities import Candidature
from ...domain.ports import (
    CandidatureRepository,
    OffreRepository,
    UtilisateurRepository,
)
from ..dto import CandidatureDTO


class ListerMesCandidaturesUseCase:
    """Use case pour lister les candidatures du candidat connecté."""

    def __init__(
        self,
        candidature_repository: CandidatureRepository,
        utilisateur_repository: UtilisateurRepository,
        offre_repository: OffreRepository,
    ):
        self._candidature_repository = candidature_repository
        self._utilisateur_repository = utilisateur_repository
        self._offre_repository = offre_repository

    async def executer(self, candidat_id: str) -> list[CandidatureDTO]:
        """Liste toutes les candidatures d'un candidat.

        Toutes les candidatures appartiennent au même candidat, on résout
        donc le nom complet une seule fois et on le partage entre elles.
        Pour chaque candidature rattachée à une offre, on résout le titre
        et la référence de cette offre.

        Args:
            candidat_id: UUID du candidat connecté (en string)

        Returns:
            list[CandidatureDTO]: les candidatures du candidat
        """
        candidat_uuid = UUID(candidat_id)

        candidatures = await self._candidature_repository.lister_par_candidat(
            candidat_uuid
        )

        candidat = await self._utilisateur_repository.obtenir_candidat_par_id(
            candidat_uuid
        )
        candidat_nom_complet = candidat.nom_complet if candidat else ""
        candidat_email = str(candidat.email) if candidat else ""

        return [
            await self._convertir_en_dto(
                candidature, candidat_nom_complet, candidat_email
            )
            for candidature in candidatures
        ]

    async def _convertir_en_dto(
        self,
        candidature: Candidature,
        candidat_nom_complet: str,
        candidat_email: str,
    ) -> CandidatureDTO:
        """Convertit une candidature en DTO de sortie."""
        offre_titre = None
        offre_numero_reference = None
        if candidature.offre_id is not None:
            offre = await self._offre_repository.obtenir_par_id(candidature.offre_id)
            if offre is not None:
                offre_titre = offre.titre
                offre_numero_reference = str(offre.numero_reference)

        return CandidatureDTO(
            id=str(candidature.id),
            numero_reference=str(candidature.numero_reference),
            candidat_nom_complet=candidat_nom_complet,
            candidat_email=candidat_email,
            offre_titre=offre_titre,
            offre_numero_reference=offre_numero_reference,
            statut=candidature.statut,
            message_motivation=candidature.message_motivation,
            notes_internes=candidature.notes_internes,
            date_soumission=candidature.date_soumission.isoformat(),
            date_derniere_modification=candidature.date_derniere_modification.isoformat(),
            documents=[],  # TODO: Récupérer les documents réels
            historique=[],  # TODO: Récupérer l'historique réel
            est_spontanee=candidature.est_spontanee(),
            est_complete=candidature.est_complete(),
        )
