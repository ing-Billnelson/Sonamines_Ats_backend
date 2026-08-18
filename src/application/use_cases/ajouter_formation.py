"""Use case pour ajouter une formation au profil candidat."""

from uuid import UUID

from ...domain.entities import Formation
from ...domain.exceptions import UtilisateurIntrouvableError
from ...domain.ports import ProfilCandidatRepository, UtilisateurRepository
from ..dto import AjouterFormationDTO, FormationDTO


class AjouterFormationUseCase:
    """Use case pour ajouter une formation à un candidat."""

    def __init__(
        self,
        utilisateur_repository: UtilisateurRepository,
        profil_candidat_repository: ProfilCandidatRepository,
    ):
        self._utilisateur_repository = utilisateur_repository
        self._profil_candidat_repository = profil_candidat_repository

    async def executer(self, donnees: AjouterFormationDTO) -> FormationDTO:
        """Ajoute une formation au candidat.

        Raises:
            UtilisateurIntrouvableError: Si le candidat n'existe pas
        """
        candidat_uuid = UUID(donnees.candidat_id)
        candidat = await self._utilisateur_repository.obtenir_candidat_par_id(
            candidat_uuid
        )
        if not candidat:
            raise UtilisateurIntrouvableError(donnees.candidat_id)

        formation = Formation.creer_nouvelle(
            candidat_id=candidat_uuid,
            etablissement=donnees.etablissement,
            diplome=donnees.diplome,
            annee_debut=donnees.annee_debut,
            annee_fin=donnees.annee_fin,
        )

        formation_sauvegarde = (
            await self._profil_candidat_repository.sauvegarder_formation(formation)
        )

        return FormationDTO(
            id=str(formation_sauvegarde.id),
            etablissement=formation_sauvegarde.etablissement,
            diplome=formation_sauvegarde.diplome,
            annee_debut=formation_sauvegarde.annee_debut,
            annee_fin=formation_sauvegarde.annee_fin,
        )
