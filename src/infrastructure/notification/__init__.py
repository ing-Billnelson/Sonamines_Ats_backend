"""Adapters de notification (email/SMS)."""

from .email_adapter import EmailAdapter
from .sms_adapter import SMSAdapter
from .notification_router import NotificationRouter

__all__ = [
    "EmailAdapter",
    "SMSAdapter",
    "NotificationRouter",
]