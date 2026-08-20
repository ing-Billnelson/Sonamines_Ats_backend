"""Use case pour soumettre une candidature spontanée."""

from uuid import UUID

from ...domain.entities import Candidature, HistoriqueStatut
from ...domain.enums import StatutCandidature, TypeEvenement
from ...domain.exceptions import UtilisateurIntrouvableError
from ...domain.ports import (
    CandidatureRepository,
    SearchPort,
    UtilisateurRepository,
)
from ..dto import CandidatureDTO, SoumettreKandidatureDTO
from .notifier_utilisateur import NotifierUtilisateurUseCase


class SoumettreCandidatureSpontaneeUseCase:
    """Use case pour soumettre une candidature spontanée."""

    def __init__(
        self,
        candidature_repository: CandidatureRepository,
        utilisateur_repository: UtilisateurRepository,
        notifier_utilisateur: NotifierUtilisateurUseCase,
        search_port: SearchPort,
    ):
        self._candidature_repository = candidature_repository
        self._utilisateur_repository = utilisateur_repository
        self._notifier_utilisateur = notifier_utilisateur
        self._search_port = search_port

    async def executer(self, donnees: SoumettreKandidatureDTO) -> CandidatureDTO:
        """
        Soumet une candidature spontanée.

        Args:
            donnees: Données de soumission de candidature

        Returns:
            CandidatureDTO: Informations de la candidature créée

        Raises:
            UtilisateurIntrouvableError: Si le candidat n'existe pas
            ValueError: Si l'offre_id est fournie (doit être None pour spontanée)
        """
        candidat_id = UUID(donnees.candidat_id)

        # Vérifier que c'est bien une candidature spontanée
        if donnees.offre_id is not None:
            raise ValueError(
                "Une candidature spontanée ne doit pas avoir d'offre associée"
            )

        # Récupérer le candidat
        candidat = await self._utilisateur_repository.obtenir_candidat_par_id(
            candidat_id
        )
        if not candidat:
            raise UtilisateurIntrouvableError(str(candidat_id))

        # Créer la candidature
        candidature = Candidature.creer_nouvelle(
            candidat_id=candidat_id,
            message_motivation=donnees.message_motivation,
            offre_id=None,  # Candidature spontanée
        )

        # Sauvegarder la candidature
        candidature_sauvegarde = await self._candidature_repository.sauvegarder(
            candidature
        )

        # Indexer la candidature dans Elasticsearch (info candidat, sans offre)
        await self._search_port.indexer_candidature(
            candidature_sauvegarde, candidat=candidat
        )

        # Créer l'historique initial
        historique = HistoriqueStatut.creer_nouveau(
            candidature_id=candidature_sauvegarde.id,
            ancien_statut=None,
            nouveau_statut=StatutCandidature.RECUE,
            utilisateur_id=candidat_id,
            commentaire="Candidature spontanée soumise",
        )
        await self._candidature_repository.sauvegarder_historique_statut(historique)

        # Notifier le candidat
        await self._notifier_utilisateur.executer(
            utilisateur=candidat,
            evenement=TypeEvenement.CANDIDATURE_RECUE,
            contenu=(
                f"Votre candidature spontanée a été reçue. "
                f"Numéro de référence: {candidature_sauvegarde.numero_reference}"
            ),
        )

        return await self._convertir_en_dto(candidature_sauvegarde, candidat)

    async def _convertir_en_dto(
        self, candidature: Candidature, candidat
    ) -> CandidatureDTO:
        """Convertit une candidature en DTO."""
        # TODO: Implémenter la récupération des documents et historique complets
        return CandidatureDTO(
            id=str(candidature.id),
            numero_reference=str(candidature.numero_reference),
            candidat_nom_complet=candidat.nom_complet,
            candidat_email=str(candidat.email),
            offre_titre=None,  # Candidature spontanée
            offre_numero_reference=None,  # Candidature spontanée
            statut=candidature.statut,
            message_motivation=candidature.message_motivation,
            notes_internes=candidature.notes_internes,
            date_soumission=candidature.date_soumission.isoformat(),
            date_derniere_modification=candidature.date_derniere_modification.isoformat(),
            documents=[],  # TODO: Récupérer les documents réels
            historique=[],  # TODO: Récupérer l'historique réel
            est_spontanee=True,
            est_complete=candidature.est_complete(),
        )