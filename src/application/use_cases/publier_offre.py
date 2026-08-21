"""Use case pour publier une offre."""

from uuid import UUID

from ...domain.exceptions import OffreIntrouvableError
from ...domain.ports import OffreRepository, SearchPort, UtilisateurRepository
from ..dto import OffreDTO


class PublierOffreUseCase:
    """Use case pour publier une offre (passer de BROUILLON à OUVERTE)."""

    def __init__(
        self,
        offre_repository: OffreRepository,
        utilisateur_repository: UtilisateurRepository,
        search_port: SearchPort,
    ):
        self._offre_repository = offre_repository
        self._utilisateur_repository = utilisateur_repository
        self._search_port = search_port

    async def executer(self, offre_id: str) -> OffreDTO:
        """Publie une offre et retourne ses informations complètes."""
        offre = await self._offre_repository.obtenir_par_id(UUID(offre_id))
        if not offre:
            raise OffreIntrouvableError(offre_id)

        # offre.publier() lève ValueError si la transition est invalide
        # (seules les offres en brouillon peuvent être publiées).
        offre.publier()

        offre_sauvegarde = await self._offre_repository.sauvegarder(offre)

        # Mettre à jour l'index (statut OUVERTE + date_publication) — best-effort
        await self._search_port.indexer_offre(offre_sauvegarde)

        createur = await self._utilisateur_repository.obtenir_par_id(
            offre_sauvegarde.createur_id
        )
        createur_nom_complet = createur.nom_complet if createur else ""

        return self._convertir_en_dto(offre_sauvegarde, createur_nom_complet)

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
            eligibilite_activee=offre.eligibilite_activee,
            niveau_academique_minimum=offre.niveau_academique_minimum,
            langues_requises=offre.langues_requises,
            disponibilite_requise=offre.disponibilite_requise,
            createur_nom_complet=createur_nom_complet,
            date_creation=offre.date_creation.isoformat(),
            date_publication=(
                offre.date_publication.isoformat() if offre.date_publication else None
            ),
            date_cloture=(
                offre.date_cloture.isoformat() if offre.date_cloture else None
            ),
        )
