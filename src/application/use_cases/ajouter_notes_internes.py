"""Use case pour ajouter des notes internes à une candidature (côté RH)."""

from uuid import UUID

from ...domain.exceptions import CandidatureIntrouvableError
from ...domain.ports import (
    CandidatureRepository,
    OffreRepository,
    UtilisateurRepository,
)
from ..dto import CandidatureDTO


class AjouterNotesInternesUseCase:
    """Use case pour ajouter des notes internes à une candidature."""

    def __init__(
        self,
        candidature_repository: CandidatureRepository,
        utilisateur_repository: UtilisateurRepository,
        offre_repository: OffreRepository,
    ):
        self._candidature_repository = candidature_repository
        self._utilisateur_repository = utilisateur_repository
        self._offre_repository = offre_repository

    async def executer(self, candidature_id: str, notes: str) -> CandidatureDTO:
        """Met à jour les notes internes d'une candidature.

        Args:
            candidature_id: UUID de la candidature (en string)
            notes: Nouveau contenu des notes internes

        Raises:
            CandidatureIntrouvableError: Si la candidature n'existe pas
        """
        candidature_uuid = UUID(candidature_id)

        candidature = await self._candidature_repository.obtenir_par_id(
            candidature_uuid
        )
        if candidature is None:
            raise CandidatureIntrouvableError(candidature_id)

        # Applique la règle métier : met à jour les notes et date de modification
        candidature.ajouter_notes_internes(notes)

        candidature_sauvegarde = await self._candidature_repository.sauvegarder(
            candidature
        )

        return await self._convertir_en_dto(candidature_sauvegarde)

    async def _convertir_en_dto(self, candidature) -> CandidatureDTO:
        """Convertit une candidature en DTO (candidat + offre résolus)."""
        candidat_nom_complet = ""
        candidat_email = ""
        candidat = await self._utilisateur_repository.obtenir_candidat_par_id(
            candidature.candidat_id
        )
        if candidat is not None:
            candidat_nom_complet = candidat.nom_complet
            candidat_email = str(candidat.email)

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
