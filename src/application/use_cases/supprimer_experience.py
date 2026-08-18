"""Use case pour supprimer une expérience du profil candidat."""

from uuid import UUID

from ...domain.exceptions import UtilisateurIntrouvableError
from ...domain.ports import ProfilCandidatRepository, UtilisateurRepository


class SupprimerExperienceUseCase:
    """Use case pour supprimer une expérience d'un candidat."""

    def __init__(
        self,
        utilisateur_repository: UtilisateurRepository,
        profil_candidat_repository: ProfilCandidatRepository,
    ):
        self._utilisateur_repository = utilisateur_repository
        self._profil_candidat_repository = profil_candidat_repository

    async def executer(self, candidat_id: str, experience_id: str) -> bool:
        """Supprime une expérience appartenant au candidat.

        Raises:
            UtilisateurIntrouvableError: Si le candidat n'existe pas
        Returns:
            bool: True si l'expérience a été supprimée, False si absente
        """
        candidat_uuid = UUID(candidat_id)
        candidat = await self._utilisateur_repository.obtenir_candidat_par_id(
            candidat_uuid
        )
        if not candidat:
            raise UtilisateurIntrouvableError(candidat_id)

        return await self._profil_candidat_repository.supprimer_experience(
            UUID(experience_id)
        )
