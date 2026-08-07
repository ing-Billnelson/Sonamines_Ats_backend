"""Adapters de notification (email/SMS)."""

from .email_adapter import EmailAdapter
from .sms_adapter import SMSAdapter

__all__ = [
    "EmailAdapter",
    "SMSAdapter",
]