"""Use case pour changer le statut d'une candidature."""

from typing import Optional
from uuid import UUID

from ...domain.entities import HistoriqueStatut
from ...domain.enums import StatutCandidature, TypeEvenement
from ...domain.exceptions import CandidatureIntrouvableError, UtilisateurIntrouvableError
from ...domain.ports import (
    CandidatureRepository,
    OffreRepository,
    SearchPort,
    UtilisateurRepository,
)
from ..dto import CandidatureDTO
from .notifier_utilisateur import NotifierUtilisateurUseCase

_EVENEMENT_PAR_STATUT: dict[StatutCandidature, TypeEvenement] = {
    StatutCandidature.RECUE: TypeEvenement.CANDIDATURE_RECUE,
    StatutCandidature.DOSSIER_COMPLET: TypeEvenement.CANDIDATURE_DOSSIER_COMPLET,
    StatutCandidature.PRESELECTIONNEE: TypeEvenement.CANDIDATURE_PRESELECTIONNEE,
    StatutCandidature.CONVOQUEE: TypeEvenement.CANDIDATURE_CONVOQUEE,
    StatutCandidature.SELECTIONNEE: TypeEvenement.CANDIDATURE_SELECTIONNEE,
    StatutCandidature.REJETEE: TypeEvenement.CANDIDATURE_REJETEE,
}


class ChangerStatutCandidatureUseCase:
    """Use case pour changer le statut d'une candidature avec historisation."""

    def __init__(
        self,
        candidature_repository: CandidatureRepository,
        notifier_utilisateur: NotifierUtilisateurUseCase,
        utilisateur_repository: UtilisateurRepository,
        offre_repository: OffreRepository,
        search_port: SearchPort,
    ):
        self._candidature_repository = candidature_repository
        self._notifier_utilisateur = notifier_utilisateur
        self._utilisateur_repository = utilisateur_repository
        self._offre_repository = offre_repository
        self._search_port = search_port

    async def executer(
        self,
        candidature_id: str,
        nouveau_statut: StatutCandidature,
        commentaire: Optional[str] = None,
        utilisateur_id: Optional[str] = None,
    ) -> CandidatureDTO:
        """Change le statut d'une candidature.

        Args:
            candidature_id: UUID de la candidature (en string)
            nouveau_statut: Nouveau statut de la candidature
            commentaire: Commentaire optionnel sur le changement
            utilisateur_id: UUID de l'admin RH effectuant le changement (optionnel)

        Raises:
            CandidatureIntrouvableError: Si la candidature n'existe pas
            UtilisateurIntrouvableError: Si le candidat n'existe pas
            ValueError: Si la transition de statut est invalide
        """
        candidature_uuid = UUID(candidature_id)
        ancien_statut = nouveau_statut

        candidature = await self._candidature_repository.obtenir_par_id(
            candidature_uuid
        )
        if candidature is None:
            raise CandidatureIntrouvableError(candidature_id)

        ancien_statut = candidature.statut

        # Applique la règle métier de transition (lève ValueError si invalide)
        candidature.changer_statut(nouveau_statut)

        candidat = await self._utilisateur_repository.obtenir_candidat_par_id(
            candidature.candidat_id
        )
        if candidat is None:
            raise UtilisateurIntrouvableError(str(candidature.candidat_id))

        candidature_sauvegarde = await self._candidature_repository.sauvegarder(
            candidature
        )

        # Ré-indexer la candidature : le statut a changé, l'index doit refléter
        # l'état à jour (avec les infos candidat et offre dénormalisées).
        offre = None
        if candidature_sauvegarde.offre_id is not None:
            offre = await self._offre_repository.obtenir_par_id(
                candidature_sauvegarde.offre_id
            )
        await self._search_port.indexer_candidature(
            candidature_sauvegarde, candidat=candidat, offre=offre
        )

        utilisateur_historique = (
            UUID(utilisateur_id) if utilisateur_id else candidature.candidat_id
        )
        historique = HistoriqueStatut.creer_nouveau(
            candidature_id=candidature_sauvegarde.id,
            ancien_statut=ancien_statut,
            nouveau_statut=nouveau_statut,
            utilisateur_id=utilisateur_historique,
            commentaire=commentaire,
        )
        await self._candidature_repository.sauvegarder_historique_statut(historique)

        evenement = self._evenement_pour_statut(nouveau_statut)
        await self._notifier_utilisateur.executer(
            utilisateur=candidat,
            evenement=evenement,
            contenu=(
                f"Le statut de votre candidature "
                f"({candidature_sauvegarde.numero_reference}) est passé à "
                f"{nouveau_statut.value}."
            ),
        )

        return await self._convertir_en_dto(candidature_sauvegarde, candidat)

    def _evenement_pour_statut(
        self, statut: StatutCandidature
    ) -> TypeEvenement:
        """Retourne l'événement de notification associé à un statut."""
        return _EVENEMENT_PAR_STATUT.get(
            statut, TypeEvenement.CANDIDATURE_RECUE
        )

    async def _convertir_en_dto(self, candidature, candidat) -> CandidatureDTO:
        """Convertit une candidature en DTO."""
        return CandidatureDTO(
            id=str(candidature.id),
            numero_reference=str(candidature.numero_reference),
            candidat_nom_complet=candidat.nom_complet,
            candidat_email=str(candidat.email),
            offre_titre=None,  # TODO: Récupérer le titre de l'offre
            offre_numero_reference=None,  # TODO: Récupérer la référence de l'offre
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
