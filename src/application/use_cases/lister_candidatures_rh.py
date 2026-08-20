"""Use case pour lister toutes les candidatures (côté RH)."""

from typing import Optional
from uuid import UUID

from ...domain.entities import Candidature
from ...domain.enums import StatutCandidature
from ...domain.ports import (
    CandidatureRepository,
    OffreRepository,
    UtilisateurRepository,
)
from ..dto import CandidatureDTO


class ListerCandidaturesRHUseCase:
    """Use case pour lister toutes les candidatures avec filtres (accès RH)."""

    def __init__(
        self,
        candidature_repository: CandidatureRepository,
        utilisateur_repository: UtilisateurRepository,
        offre_repository: OffreRepository,
    ):
        self._candidature_repository = candidature_repository
        self._utilisateur_repository = utilisateur_repository
        self._offre_repository = offre_repository

    async def executer(
        self,
        statut: Optional[StatutCandidature] = None,
        offre_id: Optional[str] = None,
        spontanee: Optional[bool] = None,
        page: int = 1,
        taille_page: int = 20,
    ) -> tuple[list[CandidatureDTO], int]:
        """Liste toutes les candidatures avec filtres optionnels et pagination.

        Les candidatures peuvent appartenir à des candidats et des offres
        différents, on résout donc les informations de chaque candidature
        individuellement (pas d'optimisation prématurée).

        Returns:
            tuple[list[CandidatureDTO], int]: les candidatures de la page et
            le nombre total correspondant aux filtres.
        """
        offre_uuid = UUID(offre_id) if offre_id is not None else None

        candidatures, total = await self._candidature_repository.lister_toutes(
            statut=statut,
            offre_id=offre_uuid,
            spontanee=spontanee,
            page=page,
            taille_page=taille_page,
        )

        dtos = [await self._convertir_en_dto(candidature) for candidature in candidatures]
        return dtos, total

    async def _convertir_en_dto(self, candidature: Candidature) -> CandidatureDTO:
        """Convertit une candidature en DTO, résout les infos candidat et offre."""
        offre_titre = None
        offre_numero_reference = None
        if candidature.offre_id is not None:
            offre = await self._offre_repository.obtenir_par_id(candidature.offre_id)
            if offre is not None:
                offre_titre = offre.titre
                offre_numero_reference = str(offre.numero_reference)

        candidat_nom_complet = ""
        candidat_email = ""
        candidat = await self._utilisateur_repository.obtenir_candidat_par_id(
            candidature.candidat_id
        )
        if candidat is not None:
            candidat_nom_complet = candidat.nom_complet
            candidat_email = str(candidat.email)

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
