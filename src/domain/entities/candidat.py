"""Entité candidat."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from ..enums import CanalNotification, StatutCompte
from ..value_objects import Email, NumeroTelephone
from .utilisateur import Utilisateur


@dataclass
class Candidat(Utilisateur):
    """Entité représentant un candidat à l'emploi ou au stage."""

    photo_url: Optional[str] = None  # URL de la photo de profil (facultative)

    @classmethod
    def creer_nouveau(
        cls,
        email: Email,
        telephone: Optional[NumeroTelephone],
        mot_de_passe_hash: str,
        nom: str,
        prenom: str,
        canal_validation: CanalNotification,
    ) -> "Candidat":
        """Crée un nouveau candidat avec les valeurs par défaut."""
        return cls(
            id=uuid4(),
            email=email,
            telephone=telephone,
            mot_de_passe_hash=mot_de_passe_hash,
            nom=nom,
            prenom=prenom,
            statut=StatutCompte.EN_ATTENTE_VALIDATION,
            canal_validation=canal_validation,
            email_verifie=False,
            telephone_verifie=False,
            date_creation=datetime.utcnow(),
            date_derniere_connexion=None,
            date_modification=None,
            photo_url=None,
        )

    def definir_photo_profil(self, photo_url: str) -> None:
        """Définit l'URL de la photo de profil du candidat."""
        self.photo_url = photo_url
        self.date_modification = datetime.utcnow()

    def supprimer_photo_profil(self) -> None:
        """Supprime la photo de profil du candidat."""
        self.photo_url = None
        self.date_modification = datetime.utcnow()

    def a_photo_profil(self) -> bool:
        """Vérifie si le candidat a une photo de profil."""
        return self.photo_url is not None