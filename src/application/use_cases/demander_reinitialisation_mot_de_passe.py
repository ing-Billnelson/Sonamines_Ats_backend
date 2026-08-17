"""Use case pour demander un code de réinitialisation du mot de passe."""

from ...domain.entities import AdministrateurRH, SuperAdministrateur
from ...domain.enums import TypeEvenement
from ...domain.ports import UtilisateurRepository
from ...domain.value_objects import Email
from ..dto import DemanderReinitialisationDTO
from .notifier_utilisateur import NotifierUtilisateurUseCase


class DemanderReinitialisationMotDePasseUseCase:
    """
    Use case pour demander un code de réinitialisation du mot de passe.

    Principe anti-énumération : si l'email n'existe pas, on retourne
    silencieusement sans lever d'exception ni révéler quoi que ce soit.
    """

    def __init__(
        self,
        utilisateur_repository: UtilisateurRepository,
        notifier_utilisateur: NotifierUtilisateurUseCase,
    ):
        self._utilisateur_repository = utilisateur_repository
        self._notifier_utilisateur = notifier_utilisateur

    async def executer(self, donnees: DemanderReinitialisationDTO) -> None:
        """Génère et envoie un code de réinitialisation si l'email existe."""
        email = Email(donnees.email)
        utilisateur = await self._utilisateur_repository.obtenir_par_email(email)

        # Anti-énumération : ne rien révéler si l'utilisateur n'existe pas.
        if not utilisateur:
            return

        utilisateur.generer_code_reinitialisation()

        # Sauvegarder les modifications selon le type concret.
        if hasattr(utilisateur, "photo_url"):  # Candidat
            utilisateur_sauvegarde = (
                await self._utilisateur_repository.sauvegarder_candidat(utilisateur)
            )
        elif isinstance(utilisateur, SuperAdministrateur):
            utilisateur_sauvegarde = (
                await self._utilisateur_repository.sauvegarder_super_admin(utilisateur)
            )
        elif isinstance(utilisateur, AdministrateurRH):
            utilisateur_sauvegarde = (
                await self._utilisateur_repository.sauvegarder_admin_rh(utilisateur)
            )
        else:
            utilisateur_sauvegarde = utilisateur

        # Notifier l'utilisateur avec son code de réinitialisation.
        await self._notifier_utilisateur.executer(
            utilisateur=utilisateur_sauvegarde,
            evenement=TypeEvenement.MOT_DE_PASSE_REINITIALISE,
            contenu=(
                f"Votre code de réinitialisation de mot de passe est : "
                f"{utilisateur_sauvegarde.code_reinitialisation}. "
                "Il expire dans 5 minutes."
            ),
        )
