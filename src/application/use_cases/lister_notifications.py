"""Use case pour lister les notifications d'un utilisateur."""

from uuid import UUID
from typing import List

from ...domain.ports import NotificationRepository
from ..dto import (
    ListerNotificationsDTO,
    NotificationDTO,
    StatistiquesNotificationsDTO,
)


class ListerNotificationsUseCase:
    """Use case pour lister les notifications d'un utilisateur."""

    def __init__(self, notification_repository: NotificationRepository):
        self._notification_repository = notification_repository

    async def executer(self, donnees: ListerNotificationsDTO) -> List[NotificationDTO]:
        """
        Liste les notifications d'un utilisateur avec pagination.

        Args:
            donnees: Critères de listage des notifications

        Returns:
            List[NotificationDTO]: Liste des notifications

        Raises:
            ValueError: Si les paramètres sont invalides
        """
        utilisateur_id = UUID(donnees.utilisateur_id)

        # Récupérer les notifications selon le filtre
        if donnees.non_lues_seulement:
            notifications = (
                await self._notification_repository.lister_non_lues_par_utilisateur(
                    utilisateur_id
                )
            )
        else:
            notifications = (
                await self._notification_repository.lister_par_utilisateur(
                    utilisateur_id=utilisateur_id,
                    limit=donnees.limit,
                    offset=donnees.offset,
                )
            )

        # Convertir en DTOs
        return [self._convertir_en_dto(notification) for notification in notifications]

    async def obtenir_statistiques(
        self, utilisateur_id: str
    ) -> StatistiquesNotificationsDTO:
        """
        Obtient les statistiques des notifications d'un utilisateur.

        Args:
            utilisateur_id: ID de l'utilisateur (UUID en string)

        Returns:
            StatistiquesNotificationsDTO: Statistiques des notifications
        """
        utilisateur_uuid = UUID(utilisateur_id)

        # Compter les notifications non lues
        nb_non_lues = await self._notification_repository.compter_non_lues_par_utilisateur(
            utilisateur_uuid
        )

        # Récupérer les notifications récentes pour obtenir la dernière
        notifications_recentes = (
            await self._notification_repository.lister_par_utilisateur(
                utilisateur_id=utilisateur_uuid,
                limit=1,
                offset=0,
            )
        )

        derniere_notification = None
        if notifications_recentes:
            derniere_notification = self._convertir_en_dto(notifications_recentes[0])

        # TODO: Implémenter le comptage total si nécessaire
        # Pour l'instant, on approxime avec les non lues
        return StatistiquesNotificationsDTO(
            total_notifications=nb_non_lues,  # Approximation
            notifications_non_lues=nb_non_lues,
            derniere_notification=derniere_notification,
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