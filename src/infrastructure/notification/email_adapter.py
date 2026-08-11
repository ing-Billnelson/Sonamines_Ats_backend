"""Adapter pour l'envoi d'emails."""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict, Any

import structlog

from ...domain.entities import Utilisateur
from ...domain.enums import CanalNotification
from ...domain.ports import NotificationPort
from ..config import Settings


class EmailAdapter(NotificationPort):
    """Adapter pour l'envoi de notifications par email."""

    def __init__(self, settings: Settings):
        self._settings = settings
        self._logger = structlog.get_logger()

    async def envoyer(
        self,
        destinataire: Utilisateur,
        canal: CanalNotification,
        contenu: str,
    ) -> bool:
        """
        Envoie une notification par email.

        Args:
            destinataire: L'utilisateur destinataire
            canal: Le canal d'envoi (doit être EMAIL)
            contenu: Le contenu du message

        Returns:
            True si l'envoi a réussi, False sinon

        Raises:
            ValueError: Si le canal n'est pas EMAIL
        """
        if canal != CanalNotification.EMAIL:
            raise ValueError(f"Canal non supporté par cet adapter: {canal}")

        try:
            # Créer le message
            message = self._creer_message_email(destinataire, contenu)
            
            # Envoyer via SMTP
            await self._envoyer_via_smtp(str(destinataire.email), message)
            
            return True

        except Exception as e:
            self._logger.error(
                "Erreur lors de l'envoi d'email",
                type=type(e).__name__,
                message=str(e),
                destinataire=str(destinataire.email),
            )
            return False

    def _creer_message_email(self, destinataire: Utilisateur, contenu: str) -> MIMEMultipart:
        """Crée un message email formaté."""
        message = MIMEMultipart("alternative")
        
        # En-têtes
        message["From"] = self._settings.smtp_from_address
        message["To"] = str(destinataire.email)
        message["Subject"] = "Notification SONAMINES - Plateforme Candidatures"

        # Corps du message
        corps_texte = f"""
Bonjour {destinataire.nom_complet},

{contenu}

Cordialement,
L'équipe SONAMINES

---
Ceci est un message automatique, merci de ne pas y répondre.
        """.strip()

        corps_html = f"""
        <html>
          <head></head>
          <body>
            <p>Bonjour <strong>{destinataire.nom_complet}</strong>,</p>
            <p>{contenu}</p>
            <p>Cordialement,<br>L'équipe SONAMINES</p>
            <hr>
            <p><em>Ceci est un message automatique, merci de ne pas y répondre.</em></p>
          </body>
        </html>
        """

        # Attacher les parties texte et HTML
        partie_texte = MIMEText(corps_texte, "plain", "utf-8")
        partie_html = MIMEText(corps_html, "html", "utf-8")

        message.attach(partie_texte)
        message.attach(partie_html)

        return message

    async def _envoyer_via_smtp(self, email_destinataire: str, message: MIMEMultipart) -> None:
        """Envoie le message via SMTP."""
        # TODO: Implémenter l'envoi asynchrone réel
        # Pour l'instant, simulation synchrone
        
        if not self._settings.smtp_username or not self._settings.smtp_password:
            raise ValueError("Configuration SMTP incomplète")

        server = None
        try:
            # Connexion au serveur SMTP
            server = smtplib.SMTP(self._settings.smtp_host, self._settings.smtp_port)
            
            if self._settings.smtp_tls:
                server.starttls()
            
            server.login(self._settings.smtp_username, self._settings.smtp_password)
            
            # Envoi du message
            server.send_message(message, to_addrs=[email_destinataire])
            
        finally:
            if server:
                server.quit()