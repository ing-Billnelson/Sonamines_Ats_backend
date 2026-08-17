"""Use case central pour la notification des utilisateurs."""

import structlog

from ...domain.entities import Notification, Utilisateur
from ...domain.enums import CanalNotification, TypeEvenement
from ...domain.exceptions import CanalNonVerifieError
from ...domain.ports import NotificationPort, NotificationRepository


class NotifierUtilisateurUseCase:
    """
    Use case central pour la notification des utilisateurs.

    Implémente la règle de gestion des notifications duales :
    1. Notification INTERNE (toujours créée et persistée)
    2. Envoi EXTERNE (email ou SMS selon le canal configuré)
    """

    def __init__(
        self,
        notification_repository: NotificationRepository,
        notification_port: NotificationPort,
    ):
        self._notification_repository = notification_repository
        self._notification_port = notification_port
        self._logger = structlog.get_logger()

    async def executer(
        self,
        utilisateur: Utilisateur,
        evenement: TypeEvenement,
        contenu: str,
    ) -> None:
        """
        Notifie un utilisateur d'un événement.

        Cette méthode suit strictement la règle de gestion :
        1. Crée TOUJOURS une notification interne
        2. Envoie EXCLUSIVEMENT via le canal configuré de l'utilisateur

        Args:
            utilisateur: L'utilisateur à notifier
            evenement: Le type d'événement
            contenu: Le contenu de la notification

        Raises:
            CanalNonVerifieError: Si le canal externe n'est pas vérifié
        """
        # 1. Notification interne : TOUJOURS créée, jamais conditionnelle
        notification_interne = Notification.creer_nouvelle(
            utilisateur_id=utilisateur.id,
            type_evenement=evenement,
            contenu=contenu,
        )

        await self._notification_repository.sauvegarder(notification_interne)

        # 2. Envoi externe : UN SEUL canal, celui actuellement configuré
        if utilisateur.canal_validation.is_external:
            # COMPTE_CREE : le code de validation est envoyé pour permettre la
            # vérification — le canal ne peut donc pas encore être vérifié, on
            # envoie directement sans passer par _canal_est_verifie().
            # MOT_DE_PASSE_REINITIALISE : le code de réinitialisation doit être
            # délivré pour permettre une récupération d'accès, indépendamment de
            # l'état de vérification du canal. On envoie donc directement aussi.
            if evenement in (TypeEvenement.COMPTE_CREE, TypeEvenement.MOT_DE_PASSE_REINITIALISE):
                pass
            # Autres événements : n'envoyer que si le canal est déjà vérifié.
            elif not self._canal_est_verifie(utilisateur):
                # Ne pas bloquer la notification interne, mais ne pas envoyer
                # L'utilisateur sera notifié via l'interface de l'erreur
                return

            # Envoyer via le canal configuré
            try:
                await self._notification_port.envoyer(
                    destinataire=utilisateur,
                    canal=utilisateur.canal_validation,
                    contenu=contenu,
                )
            except Exception as e:
                self._logger.error(
                    "Erreur lors de l'envoi externe de la notification",
                    type=type(e).__name__,
                    message=str(e),
                    utilisateur_id=str(utilisateur.id),
                    evenement=evenement.value,
                    canal=utilisateur.canal_validation.value,
                )

    def _canal_est_verifie(self, utilisateur: Utilisateur) -> bool:
        """Vérifie si le canal de validation de l'utilisateur est vérifié."""
        if utilisateur.canal_validation == CanalNotification.EMAIL:
            return utilisateur.email_verifie
        elif utilisateur.canal_validation == CanalNotification.SMS:
            return utilisateur.telephone_verifie

        # Canal INTERNE n'a pas besoin de vérification
        return True