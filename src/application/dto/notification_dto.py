"""DTOs pour la gestion des notifications."""

from dataclasses import dataclass
from typing import Optional

from ...domain.enums import TypeEvenement


@dataclass
class NotificationDTO:
    """DTO de sortie pour les informations de notification."""

    id: str
    type_evenement: TypeEvenement
    contenu: str
    statut_lu: bool
    date_creation: str  # ISO format
    date_lecture: Optional[str] = None  # ISO format


@dataclass
class ListerNotificationsDTO:
    """DTO pour les critères de listage des notifications."""

    utilisateur_id: str  # UUID en string
    limit: int = 50
    offset: int = 0
    non_lues_seulement: bool = False


@dataclass
class MarquerNotificationLueDTO:
    """DTO pour marquer une notification comme lue."""

    notification_id: str  # UUID en string
    utilisateur_id: str  # UUID en string pour vérification des droits


@dataclass
class StatistiquesNotificationsDTO:
    """DTO pour les statistiques de notifications."""

    total_notifications: int
    notifications_non_lues: int
    derniere_notification: Optional[NotificationDTO] = None