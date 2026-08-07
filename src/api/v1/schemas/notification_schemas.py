"""Schemas Pydantic pour les notifications."""

from pydantic import BaseModel, Field
from typing import Optional, List

from ....domain.enums import CanalNotification, TypeEvenement


class ModifierCanalNotificationRequest(BaseModel):
    """Schema de requête pour modifier le canal de notification."""

    canal: CanalNotification = Field(..., description="Nouveau canal de notification")

    class Config:
        json_schema_extra = {
            "example": {
                "canal": "SMS"
            }
        }


class NotificationResponse(BaseModel):
    """Schema de réponse pour une notification."""

    id: str
    type_evenement: TypeEvenement
    contenu: str
    statut_lu: bool
    date_creation: str
    date_lecture: Optional[str] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "type_evenement": "CANDIDATURE_RECUE",
                "contenu": "Votre candidature spontanée a été reçue. Numéro de référence: CAND-2024-ABC12345",
                "statut_lu": False,
                "date_creation": "2024-01-15T10:30:00Z",
                "date_lecture": None
            }
        }


class StatistiquesNotificationsResponse(BaseModel):
    """Schema de réponse pour les statistiques de notifications."""

    total_notifications: int
    notifications_non_lues: int
    derniere_notification: Optional[NotificationResponse] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "total_notifications": 25,
                "notifications_non_lues": 3,
                "derniere_notification": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "type_evenement": "CANDIDATURE_RECUE",
                    "contenu": "Votre candidature a été reçue",
                    "statut_lu": False,
                    "date_creation": "2024-01-15T10:30:00Z"
                }
            }
        }


class MarquerLueRequest(BaseModel):
    """Schema de requête pour marquer une notification comme lue."""

    pass  # Pas de corps de requête, l'ID est dans l'URL


class NotificationsListResponse(BaseModel):
    """Schema de réponse pour la liste des notifications."""

    notifications: List[NotificationResponse]
    total: int
    page: int
    taille_page: int
    pages_total: int

    class Config:
        from_attributes = True