"""Routeur de notifications qui délègue aux adapters appropriés selon le canal."""

from ...domain.entities import Utilisateur
from ...domain.enums import CanalNotification
from ...domain.ports import NotificationPort
from .email_adapter import EmailAdapter
from .sms_adapter import SMSAdapter


class NotificationRouter(NotificationPort):
    """
    Routeur de notifications qui délègue aux adapters appropriés selon le canal.
    
    Implémente le pattern Strategy pour router les notifications vers
    le bon adapter (EmailAdapter ou SMSAdapter) selon le canal demandé.
    """

    def __init__(self, email_adapter: EmailAdapter, sms_adapter: SMSAdapter):
        """
        Initialise le routeur avec les adapters de notification.
        
        Args:
            email_adapter: Adapter pour l'envoi d'emails
            sms_adapter: Adapter pour l'envoi de SMS
        """
        self._email_adapter = email_adapter
        self._sms_adapter = sms_adapter

    async def envoyer(
        self,
        destinataire: Utilisateur,
        canal: CanalNotification,
        contenu: str,
    ) -> bool:
        """
        Envoie une notification via le canal approprié.

        Args:
            destinataire: L'utilisateur destinataire
            canal: Le canal d'envoi (EMAIL, SMS, ou INTERNE)
            contenu: Le contenu du message à envoyer

        Returns:
            True si l'envoi a réussi, False sinon

        Raises:
            ValueError: Si le canal n'est pas supporté pour l'envoi externe
            CanalNonVerifieError: Si le canal n'est pas vérifié pour l'utilisateur
        """
        if canal == CanalNotification.EMAIL:
            return await self._email_adapter.envoyer(destinataire, canal, contenu)
        
        elif canal == CanalNotification.SMS:
            return await self._sms_adapter.envoyer(destinataire, canal, contenu)
        
        elif canal == CanalNotification.INTERNE:
            raise ValueError(
                "Le canal INTERNE ne nécessite pas d'envoi externe. "
                "Les notifications internes sont gérées par le NotificationRepository."
            )
        
        else:
            raise ValueError(
                f"Canal de notification non supporté: {canal}. "
                f"Canaux supportés: {CanalNotification.EMAIL.value}, {CanalNotification.SMS.value}"
            )