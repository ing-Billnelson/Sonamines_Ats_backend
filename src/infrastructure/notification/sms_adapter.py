"""Adapter pour l'envoi de SMS."""

import httpx
from typing import Dict, Any

from ...domain.entities import Utilisateur
from ...domain.enums import CanalNotification
from ...domain.ports import NotificationPort
from ..config import Settings


class SMSAdapter(NotificationPort):
    """Adapter pour l'envoi de notifications par SMS."""

    def __init__(self, settings: Settings):
        self._settings = settings

    async def envoyer(
        self,
        destinataire: Utilisateur,
        canal: CanalNotification,
        contenu: str,
    ) -> bool:
        """
        Envoie une notification par SMS.

        Args:
            destinataire: L'utilisateur destinataire
            canal: Le canal d'envoi (doit être SMS)
            contenu: Le contenu du message

        Returns:
            True si l'envoi a réussi, False sinon

        Raises:
            ValueError: Si le canal n'est pas SMS
        """
        if canal != CanalNotification.SMS:
            raise ValueError(f"Canal non supporté par cet adapter: {canal}")

        try:
            # Préparer le message SMS
            message_sms = self._preparer_message_sms(destinataire, contenu)
            
            # Envoyer via API SMS
            await self._envoyer_via_api(str(destinataire.telephone), message_sms)
            
            return True

        except Exception as e:
            # TODO: Logger l'erreur
            print(f"Erreur lors de l'envoi de SMS: {e}")
            return False

    def _preparer_message_sms(self, destinataire: Utilisateur, contenu: str) -> str:
        """Prépare le message SMS (limite de caractères)."""
        # Limiter la longueur du message SMS (160 caractères standard)
        prefixe = f"SONAMINES - {destinataire.prenom}: "
        suffixe = " [Ne pas répondre]"
        
        longueur_disponible = 160 - len(prefixe) - len(suffixe)
        
        if len(contenu) > longueur_disponible:
            contenu_tronque = contenu[:longueur_disponible-3] + "..."
        else:
            contenu_tronque = contenu
        
        return f"{prefixe}{contenu_tronque}{suffixe}"

    async def _envoyer_via_api(self, numero_telephone: str, message: str) -> None:
        """Envoie le SMS via l'API configurée."""
        if not self._settings.sms_api_key or not self._settings.sms_api_url:
            raise ValueError("Configuration SMS incomplète")

        # Préparer la requête API
        headers = {
            "Authorization": f"Bearer {self._settings.sms_api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "to": numero_telephone,
            "message": message,
            "from": "SONAMINES",  # Nom de l'expéditeur
        }

        # Envoyer la requête
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self._settings.sms_api_url,
                json=payload,
                headers=headers,
                timeout=10.0,
            )
            
            # Vérifier le statut de la réponse
            if response.status_code not in [200, 201, 202]:
                raise ValueError(
                    f"Échec de l'envoi SMS: {response.status_code} - {response.text}"
                )