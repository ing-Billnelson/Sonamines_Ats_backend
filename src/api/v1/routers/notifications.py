"""Router pour les notifications."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List

from ....application.use_cases import (
    ListerNotificationsUseCase,
    MarquerNotificationLueUseCase,
)
from ....application.dto import (
    ListerNotificationsDTO,
    MarquerNotificationLueDTO,
)
from ....domain.exceptions import (
    UtilisateurIntrouvableError,
    AutorisationRefuseeError,
)
from ..schemas import (
    NotificationResponse,
    NotificationsListResponse,
    StatistiquesNotificationsResponse,
    SuccessResponse,
)
from ..dependencies import (
    get_utilisateur_courant,
    get_lister_notifications_use_case,
    get_marquer_notification_lue_use_case,
)

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get(
    "",
    response_model=NotificationsListResponse,
    summary="Lister les notifications",
    description="Liste les notifications de l'utilisateur connecté avec pagination",
)
async def lister_notifications(
    page: int = Query(1, ge=1, description="Numéro de page"),
    taille_page: int = Query(20, ge=1, le=100, description="Nombre d'éléments par page"),
    non_lues_seulement: bool = Query(False, description="Afficher seulement les non lues"),
    utilisateur_courant = Depends(get_utilisateur_courant),
    use_case: ListerNotificationsUseCase = Depends(get_lister_notifications_use_case),
):
    """Liste les notifications de l'utilisateur."""
    try:
        # Convertir en DTO
        dto = ListerNotificationsDTO(
            utilisateur_id=utilisateur_courant.id,
            limit=taille_page,
            offset=(page - 1) * taille_page,
            non_lues_seulement=non_lues_seulement,
        )

        # Exécuter le use case
        notifications_dto = await use_case.executer(dto)

        # Convertir en schemas de réponse
        notifications_response = [
            NotificationResponse(
                id=notif.id,
                type_evenement=notif.type_evenement,
                contenu=notif.contenu,
                statut_lu=notif.statut_lu,
                date_creation=notif.date_creation,
                date_lecture=notif.date_lecture,
            )
            for notif in notifications_dto
        ]

        # TODO: Calculer les métadonnées de pagination
        total = len(notifications_dto)  # Approximation
        pages_total = (total + taille_page - 1) // taille_page

        return NotificationsListResponse(
            notifications=notifications_response,
            total=total,
            page=page,
            taille_page=taille_page,
            pages_total=pages_total,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "InternalError", "message": str(e)},
        )


@router.get(
    "/statistiques",
    response_model=StatistiquesNotificationsResponse,
    summary="Statistiques des notifications",
    description="Obtient les statistiques des notifications de l'utilisateur",
)
async def obtenir_statistiques_notifications(
    utilisateur_courant = Depends(get_utilisateur_courant),
    use_case: ListerNotificationsUseCase = Depends(get_lister_notifications_use_case),
):
    """Obtient les statistiques des notifications."""
    try:
        # Exécuter le use case pour obtenir les stats
        stats_dto = await use_case.obtenir_statistiques(utilisateur_courant.id)

        # Convertir la dernière notification si elle existe
        derniere_notification = None
        if stats_dto.derniere_notification:
            derniere_notification = NotificationResponse(
                id=stats_dto.derniere_notification.id,
                type_evenement=stats_dto.derniere_notification.type_evenement,
                contenu=stats_dto.derniere_notification.contenu,
                statut_lu=stats_dto.derniere_notification.statut_lu,
                date_creation=stats_dto.derniere_notification.date_creation,
                date_lecture=stats_dto.derniere_notification.date_lecture,
            )

        return StatistiquesNotificationsResponse(
            total_notifications=stats_dto.total_notifications,
            notifications_non_lues=stats_dto.notifications_non_lues,
            derniere_notification=derniere_notification,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "InternalError", "message": str(e)},
        )


@router.patch(
    "/{notification_id}/lue",
    response_model=NotificationResponse,
    summary="Marquer comme lue",
    description="Marque une notification comme lue",
)
async def marquer_notification_lue(
    notification_id: str,
    utilisateur_courant = Depends(get_utilisateur_courant),
    use_case: MarquerNotificationLueUseCase = Depends(get_marquer_notification_lue_use_case),
):
    """Marque une notification comme lue."""
    try:
        # Convertir en DTO
        dto = MarquerNotificationLueDTO(
            notification_id=notification_id,
            utilisateur_id=utilisateur_courant.id,
        )

        # Exécuter le use case
        notification_dto = await use_case.executer(dto)

        return NotificationResponse(
            id=notification_dto.id,
            type_evenement=notification_dto.type_evenement,
            contenu=notification_dto.contenu,
            statut_lu=notification_dto.statut_lu,
            date_creation=notification_dto.date_creation,
            date_lecture=notification_dto.date_lecture,
        )

    except UtilisateurIntrouvableError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "NotificationIntrouvable", "message": str(e)},
        )
    except AutorisationRefuseeError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": "AutorisationRefusee", "message": str(e)},
        )


@router.patch(
    "/toutes-lues",
    response_model=SuccessResponse,
    summary="Marquer toutes comme lues",
    description="Marque toutes les notifications de l'utilisateur comme lues",
)
async def marquer_toutes_notifications_lues(
    utilisateur_courant = Depends(get_utilisateur_courant),
    use_case: MarquerNotificationLueUseCase = Depends(get_marquer_notification_lue_use_case),
):
    """Marque toutes les notifications comme lues."""
    try:
        # Exécuter le use case
        nombre_marquees = await use_case.marquer_toutes_comme_lues(utilisateur_courant.id)

        return SuccessResponse(
            success=True,
            message=f"{nombre_marquees} notifications marquées comme lues",
            data={"nombre_marquees": nombre_marquees},
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "InternalError", "message": str(e)},
        )