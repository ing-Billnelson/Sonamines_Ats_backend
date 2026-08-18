"""Use case pour ajouter une expérience professionnelle au profil candidat."""

from datetime import datetime
from uuid import UUID

from ...domain.entities import Experience
from ...domain.exceptions import UtilisateurIntrouvableError
from ...domain.ports import ProfilCandidatRepository, UtilisateurRepository
from ..dto import AjouterExperienceDTO, ExperienceDTO


class AjouterExperienceUseCase:
    """Use case pour ajouter une expérience à un candidat."""

    def __init__(
        self,
        utilisateur_repository: UtilisateurRepository,
        profil_candidat_repository: ProfilCandidatRepository,
    ):
        self._utilisateur_repository = utilisateur_repository
        self._profil_candidat_repository = profil_candidat_repository

    async def executer(self, donnees: AjouterExperienceDTO) -> ExperienceDTO:
        """Ajoute une expérience au candidat.

        Raises:
            UtilisateurIntrouvableError: Si le candidat n'existe pas
        """
        candidat_uuid = UUID(donnees.candidat_id)
        candidat = await self._utilisateur_repository.obtenir_candidat_par_id(
            candidat_uuid
        )
        if not candidat:
            raise UtilisateurIntrouvableError(donnees.candidat_id)

        date_debut = datetime.fromisoformat(donnees.date_debut)
        date_fin = (
            datetime.fromisoformat(donnees.date_fin) if donnees.date_fin else None
        )

        experience = Experience.creer_nouvelle(
            candidat_id=candidat_uuid,
            entreprise=donnees.entreprise,
            poste=donnees.poste,
            date_debut=date_debut,
            date_fin=date_fin,
            description=donnees.description,
        )

        experience_sauvegarde = (
            await self._profil_candidat_repository.sauvegarder_experience(experience)
        )

        return ExperienceDTO(
            id=str(experience_sauvegarde.id),
            entreprise=experience_sauvegarde.entreprise,
            poste=experience_sauvegarde.poste,
            date_debut=experience_sauvegarde.date_debut.isoformat(),
            date_fin=(
                experience_sauvegarde.date_fin.isoformat()
                if experience_sauvegarde.date_fin
                else None
            ),
            description=experience_sauvegarde.description,
        )
