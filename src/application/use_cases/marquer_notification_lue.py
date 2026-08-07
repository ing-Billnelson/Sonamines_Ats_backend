"""Use case pour marquer une notification comme lue."""

from uuid import UUID

from ...domain.exceptions import (
    UtilisateurIntrouvableError,
    AutorisationRefuseeError,
)
from ...domain.ports import NotificationRepository
from ..dto import MarquerNotificationLueDTO, NotificationDTO


class MarquerNotificationLueUseCase:
    """Use case pour marquer une notification comme lue."""

    def __init__(self, notification_repository: NotificationRepository):
        self._notification_repository = notification_repository

    async def executer(self, donnees: MarquerNotificationLueDTO) -> NotificationDTO:
        """
        Marque une notification comme lue.

        Args:
            donnees: Données de marquage de notification

        Returns:
            NotificationDTO: Notification mise à jour

        Raises:
            UtilisateurIntrouvableError: Si la notification n'existe pas
            AutorisationRefuseeError: Si l'utilisateur n'est pas propriétaire
        """
        notification_id = UUID(donnees.notification_id)
        utilisateur_id = UUID(donnees.utilisateur_id)

        # Récupérer la notification
        notification = await self._notification_repository.obtenir_par_id(
            notification_id
        )

        if not notification:
            raise UtilisateurIntrouvableError(
                f"Notification {donnees.notification_id} introuvable"
            )

        # Vérifier que l'utilisateur est propriétaire de la notification
        if notification.utilisateur_id != utilisateur_id:
            raise AutorisationRefuseeError(
                "Vous ne pouvez pas modifier cette notification"
            )

        # Marquer comme lue
        notification.marquer_comme_lue()

        # Sauvegarder
        notification_sauvegarde = await self._notification_repository.sauvegarder(
            notification
        )

        return self._convertir_en_dto(notification_sauvegarde)

    async def marquer_toutes_comme_lues(self, utilisateur_id: str) -> int:
        """
        Marque toutes les notifications d'un utilisateur comme lues.

        Args:
            utilisateur_id: ID de l'utilisateur (UUID en string)

        Returns:
            int: Nombre de notifications marquées comme lues
        """
        utilisateur_uuid = UUID(utilisateur_id)

        return await self._notification_repository.marquer_toutes_comme_lues(
            utilisateur_uuid
        )

    def _convertir_en_dto(self, notification) -> NotificationDTO:
        """Convertit une notification en DTO."""
        return NotificationDTO(
            id=str(notification.id),
            type_evenement=notification.type_evenement,
            contenu=notification.contenu,
            statut_lu=notification.statut_lu,
            date_creation=notification.date_creation.isoformat(),
            date_lecture=(
                notification.date_lecture.isoformat()
                if notification.date_lecture
                else None
            ),
        )