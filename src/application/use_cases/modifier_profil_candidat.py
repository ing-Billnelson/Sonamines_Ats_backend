"""Use case pour la modification du profil candidat."""

from datetime import datetime
from uuid import UUID

from ...domain.exceptions import UtilisateurIntrouvableError
from ...domain.ports import ProfilCandidatRepository, UtilisateurRepository
from ...domain.value_objects import NumeroTelephone
from ..dto import ModifierProfilDTO, UtilisateurDTO
from .profil_candidat_conversion import convertir_candidat_profil_en_dto


class ModifierProfilCandidatUseCase:
    """Use case pour modifier les informations simples du profil candidat."""

    def __init__(
        self,
        utilisateur_repository: UtilisateurRepository,
        profil_candidat_repository: ProfilCandidatRepository,
    ):
        self._utilisateur_repository = utilisateur_repository
        self._profil_candidat_repository = profil_candidat_repository

    async def executer(self, donnees: ModifierProfilDTO) -> UtilisateurDTO:
        """Met à jour les champs fournis du profil candidat.

        Raises:
            UtilisateurIntrouvableError: Si le candidat n'existe pas
        """
        candidat_uuid = UUID(donnees.candidat_id)
        candidat = await self._utilisateur_repository.obtenir_candidat_par_id(
            candidat_uuid
        )

        if not candidat:
            raise UtilisateurIntrouvableError(donnees.candidat_id)

        # Mise à jour directe des champs fournis (non None)
        if donnees.nom is not None:
            candidat.nom = donnees.nom
        if donnees.prenom is not None:
            candidat.prenom = donnees.prenom
        if donnees.telephone is not None:
            candidat.telephone = NumeroTelephone(donnees.telephone)
        if donnees.linkedin_url is not None:
            candidat.linkedin_url = donnees.linkedin_url
        if donnees.adresse is not None:
            candidat.adresse = donnees.adresse
        if donnees.competences is not None:
            candidat.competences = donnees.competences

        candidat.date_modification = datetime.utcnow()

        candidat_sauvegarde = await self._utilisateur_repository.sauvegarder_candidat(
            candidat
        )

        return await convertir_candidat_profil_en_dto(
            candidat_sauvegarde, self._profil_candidat_repository
        )
