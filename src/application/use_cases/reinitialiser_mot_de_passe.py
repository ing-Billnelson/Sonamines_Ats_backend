"""Use case pour réinitialiser le mot de passe d'un utilisateur."""

from argon2 import PasswordHasher

from ...domain.entities import AdministrateurRH, SuperAdministrateur
from ...domain.exceptions import (
    CodeReinitialisationInvalideError,
    UtilisateurIntrouvableError,
)
from ...domain.ports import UtilisateurRepository
from ...domain.value_objects import Email
from ..dto import ReinitialiserMotDePasseDTO


class ReinitialiserMotDePasseUseCase:
    """Use case pour réinitialiser le mot de passe avec un code."""

    def __init__(
        self,
        utilisateur_repository: UtilisateurRepository,
        password_hasher: PasswordHasher,
    ):
        self._utilisateur_repository = utilisateur_repository
        self._password_hasher = password_hasher

    async def executer(self, donnees: ReinitialiserMotDePasseDTO) -> None:
        """Réinitialise le mot de passe après vérification du code.

        Raises:
            UtilisateurIntrouvableError: Si l'utilisateur n'existe pas
            CodeReinitialisationInvalideError: Si le code est incorrect ou expiré
        """
        email = Email(donnees.email)
        utilisateur = await self._utilisateur_repository.obtenir_par_email(email)

        if not utilisateur:
            raise UtilisateurIntrouvableError(donnees.email)

        # Vérifier le code de réinitialisation
        if not utilisateur.code_reinitialisation_est_valide(
            donnees.code_reinitialisation
        ):
            raise CodeReinitialisationInvalideError()

        # Hacher le nouveau mot de passe
        nouveau_hash = self._password_hasher.hash(donnees.nouveau_mot_de_passe)

        # Réinitialiser le mot de passe et invalider le code
        utilisateur.reinitialiser_mot_de_passe(nouveau_hash)

        # Sauvegarder les modifications selon le type concret.
        if hasattr(utilisateur, "photo_url"):  # Candidat
            await self._utilisateur_repository.sauvegarder_candidat(utilisateur)
        elif isinstance(utilisateur, SuperAdministrateur):
            await self._utilisateur_repository.sauvegarder_super_admin(utilisateur)
        elif isinstance(utilisateur, AdministrateurRH):
            await self._utilisateur_repository.sauvegarder_admin_rh(utilisateur)
