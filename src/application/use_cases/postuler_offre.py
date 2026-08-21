"""Use case pour postuler à une offre."""

from uuid import UUID

from sqlalchemy.exc import IntegrityError

from ...domain.entities import Candidature, HistoriqueStatut
from ...domain.enums import StatutCandidature, TypeEvenement
from ...domain.exceptions import (
    CandidatNonEligibleError,
    CandidatureDejaExistanteError,
    OffreClotureeError,
    OffreIntrouvableError,
    UtilisateurIntrouvableError,
)
from ...domain.ports import (
    CandidatureRepository,
    OffreRepository,
    SearchPort,
    UtilisateurRepository,
)
from ..dto import CandidatureDTO, SoumettreKandidatureDTO
from .notifier_utilisateur import NotifierUtilisateurUseCase


class PostulerOffreUseCase:
    """Use case pour postuler à une offre d'emploi ou de stage."""

    def __init__(
        self,
        candidature_repository: CandidatureRepository,
        offre_repository: OffreRepository,
        utilisateur_repository: UtilisateurRepository,
        notifier_utilisateur: NotifierUtilisateurUseCase,
        search_port: SearchPort,
    ):
        self._candidature_repository = candidature_repository
        self._offre_repository = offre_repository
        self._utilisateur_repository = utilisateur_repository
        self._notifier_utilisateur = notifier_utilisateur
        self._search_port = search_port

    async def executer(self, donnees: SoumettreKandidatureDTO) -> CandidatureDTO:
        """Crée une candidature pour une offre et retourne ses informations."""
        candidat_id = UUID(donnees.candidat_id)
        offre_id = UUID(donnees.offre_id)

        # Récupérer l'offre
        offre = await self._offre_repository.obtenir_par_id(offre_id)
        if not offre:
            raise OffreIntrouvableError(str(offre_id))

        # Vérifier que l'offre peut recevoir des candidatures
        if not offre.statut.is_active:
            raise OffreClotureeError()

        if offre.est_expiree():
            raise OffreClotureeError(
                "La date limite de candidature pour cette offre est dépassée"
            )

        # Récupérer le candidat
        candidat = await self._utilisateur_repository.obtenir_candidat_par_id(
            candidat_id
        )
        if not candidat:
            raise UtilisateurIntrouvableError(str(candidat_id))

        # Vérifier l'éligibilité du candidat aux critères de l'offre
        eligible, criteres_manquants = offre.verifier_eligibilite(candidat)
        if not eligible:
            raise CandidatNonEligibleError(criteres_manquants)

        # Calculer le score d'éligibilité (0-100) si le contrôle est activé
        score_eligibilite = None
        if offre.eligibilite_activee:
            score_eligibilite = offre.calculer_score_eligibilite(candidat)

        # Créer la candidature (avec offre_id renseigné)
        candidature = Candidature.creer_nouvelle(
            candidat_id=candidat_id,
            message_motivation=donnees.message_motivation,
            offre_id=offre_id,
        )
        candidature.score_eligibilite = score_eligibilite

        # Sauvegarder la candidature ; la contrainte unique (candidat_id, offre_id)
        # en base convertit une violation en exception domaine claire.
        try:
            candidature_sauvegarde = await self._candidature_repository.sauvegarder(
                candidature
            )
        except IntegrityError:
            raise CandidatureDejaExistanteError()

        # Indexer la candidature dans Elasticsearch (avec info candidat et offre)
        await self._search_port.indexer_candidature(
            candidature_sauvegarde, candidat=candidat, offre=offre
        )

        # Créer l'historique initial
        historique = HistoriqueStatut.creer_nouveau(
            candidature_id=candidature_sauvegarde.id,
            ancien_statut=None,
            nouveau_statut=StatutCandidature.RECUE,
            utilisateur_id=candidat_id,
            commentaire="Candidature soumise via l'offre",
        )
        await self._candidature_repository.sauvegarder_historique_statut(historique)

        # Notifier le candidat
        await self._notifier_utilisateur.executer(
            utilisateur=candidat,
            evenement=TypeEvenement.CANDIDATURE_RECUE,
            contenu=(
                f"Votre candidature pour l'offre '{offre.titre}' a été reçue. "
                f"Numéro de référence: {candidature_sauvegarde.numero_reference}"
            ),
        )

        return self._convertir_en_dto(candidature_sauvegarde, candidat, offre)

    def _convertir_en_dto(
        self, candidature: Candidature, candidat, offre
    ) -> CandidatureDTO:
        """Convertit une candidature en DTO."""
        return CandidatureDTO(
            id=str(candidature.id),
            numero_reference=str(candidature.numero_reference),
            candidat_nom_complet=candidat.nom_complet,
            candidat_email=str(candidat.email),
            offre_titre=offre.titre,
            offre_numero_reference=str(offre.numero_reference),
            statut=candidature.statut,
            message_motivation=candidature.message_motivation,
            notes_internes=candidature.notes_internes,
            date_soumission=candidature.date_soumission.isoformat(),
            date_derniere_modification=candidature.date_derniere_modification.isoformat(),
            documents=[],  # TODO: Récupérer les documents réels
            historique=[],  # TODO: Récupérer l'historique réel
            est_spontanee=False,
            est_complete=candidature.est_complete(),
        )
