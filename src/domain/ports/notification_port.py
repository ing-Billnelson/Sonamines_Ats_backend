"""Port pour l'envoi de notifications externes (email/SMS)."""

from abc import ABC, abstractmethod

from ..entities import Utilisateur
from ..enums import CanalNotification


class NotificationPort(ABC):
    """Interface pour l'envoi de notifications externes."""

    @abstractmethod
    async def envoyer(
        self,
        destinataire: Utilisateur,
        canal: CanalNotification,
        contenu: str,
    ) -> bool:
        """
        Envoie une notification externe via le canal spécifié.

        Args:
            destinataire: L'utilisateur destinataire
            canal: Le canal d'envoi (EMAIL ou SMS)
            contenu: Le contenu du message à envoyer

        Returns:
            True si l'envoi a réussi, False sinon

        Raises:
            CanalNonVerifieError: Si le canal n'est pas vérifié pour l'utilisateur
        """
        pass