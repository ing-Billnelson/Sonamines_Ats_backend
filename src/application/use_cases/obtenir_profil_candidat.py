"""Use case pour récupérer le profil complet d'un candidat."""

from uuid import UUID

from ...domain.exceptions import UtilisateurIntrouvableError
from ...domain.ports import ProfilCandidatRepository, UtilisateurRepository
from ..dto import UtilisateurDTO
from .profil_candidat_conversion import convertir_candidat_profil_en_dto


class ObtenirProfilCandidatUseCase:
    """Use case pour récupérer le profil complet d'un candidat (avec formations/expériences)."""

    def __init__(
        self,
        utilisateur_repository: UtilisateurRepository,
        profil_candidat_repository: ProfilCandidatRepository,
    ):
        self._utilisateur_repository = utilisateur_repository
        self._profil_candidat_repository = profil_candidat_repository

    async def executer(self, candidat_id: str) -> UtilisateurDTO:
        """Retourne le profil complet du candidat.

        Raises:
            UtilisateurIntrouvableError: Si le candidat n'existe pas
        """
        candidat_uuid = UUID(candidat_id)
        candidat = await self._utilisateur_repository.obtenir_candidat_par_id(
            candidat_uuid
        )

        if not candidat:
            raise UtilisateurIntrouvableError(candidat_id)

        return await convertir_candidat_profil_en_dto(
            candidat, self._profil_candidat_repository
        )
