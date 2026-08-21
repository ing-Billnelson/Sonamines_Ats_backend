"""Use case pour créer une offre."""

from datetime import datetime, timezone
from uuid import UUID

from ...domain.entities import Offre
from ...domain.ports import OffreRepository, SearchPort, UtilisateurRepository
from ..dto import CreerOffreDTO, OffreDTO


class CreerOffreUseCase:
    """Use case pour créer une nouvelle offre d'emploi ou de stage."""

    def __init__(
        self,
        offre_repository: OffreRepository,
        utilisateur_repository: UtilisateurRepository,
        search_port: SearchPort,
    ):
        self._offre_repository = offre_repository
        self._utilisateur_repository = utilisateur_repository
        self._search_port = search_port

    async def executer(self, donnees: CreerOffreDTO, createur_id: str) -> OffreDTO:
        """Crée une offre et retourne ses informations complètes."""
        # Convertir la date limite ISO en datetime naïf si présente
        date_limite = None
        if donnees.date_limite_candidature:
            dt = datetime.fromisoformat(donnees.date_limite_candidature)
            # Normaliser en UTC puis retirer le fuseau pour rester cohérent
            # avec les datetime naïfs (datetime.utcnow()) du reste du système,
            # requis par la colonne TIMESTAMP WITHOUT TIME ZONE.
            if dt.tzinfo is not None:
                dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
            date_limite = dt

        createur_uuid = UUID(createur_id)

        # Offre.creer_nouvelle lève ValueError si la validation EMPLOI/STAGE échoue.
        offre = Offre.creer_nouvelle(
            titre=donnees.titre,
            description=donnees.description,
            type_offre=donnees.type_offre,
            lieu=donnees.lieu,
            createur_id=createur_uuid,
            type_contrat=donnees.type_contrat,
            type_stage=donnees.type_stage,
            date_limite_candidature=date_limite,
            salaire_min=donnees.salaire_min,
            salaire_max=donnees.salaire_max,
            competences_requises=donnees.competences_requises,
            experience_requise=donnees.experience_requise,
            eligibilite_activee=donnees.eligibilite_activee,
            niveau_academique_minimum=donnees.niveau_academique_minimum,
            langues_requises=donnees.langues_requises,
            disponibilite_requise=donnees.disponibilite_requise,
        )

        offre_sauvegarde = await self._offre_repository.sauvegarder(offre)

        # Indexer l'offre dans le moteur de recherche (best-effort)
        await self._search_port.indexer_offre(offre_sauvegarde)

        # Récupérer le créateur pour le nom complet
        createur = await self._utilisateur_repository.obtenir_par_id(createur_uuid)
        createur_nom_complet = createur.nom_complet if createur else ""

        return OffreDTO(
            id=str(offre_sauvegarde.id),
            numero_reference=str(offre_sauvegarde.numero_reference),
            titre=offre_sauvegarde.titre,
            description=offre_sauvegarde.description,
            type_offre=offre_sauvegarde.type_offre,
            type_contrat=offre_sauvegarde.type_contrat,
            type_stage=offre_sauvegarde.type_stage,
            statut=offre_sauvegarde.statut,
            date_limite_candidature=(
                offre_sauvegarde.date_limite_candidature.isoformat()
                if offre_sauvegarde.date_limite_candidature
                else None
            ),
            lieu=offre_sauvegarde.lieu,
            salaire_min=offre_sauvegarde.salaire_min,
            salaire_max=offre_sauvegarde.salaire_max,
            competences_requises=offre_sauvegarde.competences_requises,
            experience_requise=offre_sauvegarde.experience_requise,
            eligibilite_activee=offre_sauvegarde.eligibilite_activee,
            niveau_academique_minimum=offre_sauvegarde.niveau_academique_minimum,
            langues_requises=offre_sauvegarde.langues_requises,
            disponibilite_requise=offre_sauvegarde.disponibilite_requise,
            createur_nom_complet=createur_nom_complet,
            date_creation=offre_sauvegarde.date_creation.isoformat(),
            date_publication=(
                offre_sauvegarde.date_publication.isoformat()
                if offre_sauvegarde.date_publication
                else None
            ),
            date_cloture=(
                offre_sauvegarde.date_cloture.isoformat()
                if offre_sauvegarde.date_cloture
                else None
            ),
        )
