"""Énumération des canaux de notification disponibles."""

from enum import Enum


class CanalNotification(str, Enum):
    """Canaux de notification disponibles pour les utilisateurs."""

    EMAIL = "EMAIL"
    SMS = "SMS"
    INTERNE = "INTERNE"  # Notifications dans l'application uniquement

    def __str__(self) -> str:
        return self.value

    @property
    def is_external(self) -> bool:
        """Vérifie si le canal nécessite un envoi externe."""
        return self in {CanalNotification.EMAIL, CanalNotification.SMS}