"""Entité utilisateur abstraite."""

from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from ..enums import CanalNotification, StatutCompte
from ..value_objects import Email, NumeroTelephone


@dataclass
class Utilisateur(ABC):
    """Entité abstraite représentant un utilisateur du système."""

    id: UUID
    email: Email
    telephone: Optional[NumeroTelephone]
    mot_de_passe_hash: str
    nom: str
    prenom: str
    statut: StatutCompte
    canal_validation: CanalNotification
    email_verifie: bool
    telephone_verifie: bool
    date_creation: datetime
    date_derniere_connexion: Optional[datetime] = None
    date_modification: Optional[datetime] = None

    @classmethod
    def creer_nouveau(
        cls,
        email: Email,
        telephone: Optional[NumeroTelephone],
        mot_de_passe_hash: str,
        nom: str,
        prenom: str,
        canal_validation: CanalNotification,
    ) -> "Utilisateur":
        """Crée un nouvel utilisateur avec les valeurs par défaut."""
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
        )

    def valider_compte(self) -> None:
        """Valide le compte utilisateur."""
        if self.canal_validation == CanalNotification.EMAIL:
            self.email_verifie = True
        elif self.canal_validation == CanalNotification.SMS:
            self.telephone_verifie = True

        self.statut = StatutCompte.ACTIF
        self.date_modification = datetime.utcnow()

    def changer_canal_validation(self, nouveau_canal: CanalNotification) -> None:
        """Change le canal de validation de l'utilisateur."""
        if nouveau_canal == CanalNotification.EMAIL and not self.email_verifie:
            raise ValueError("L'email doit être vérifié pour utiliser ce canal")
        if nouveau_canal == CanalNotification.SMS and not self.telephone_verifie:
            raise ValueError("Le téléphone doit être vérifié pour utiliser ce canal")

        self.canal_validation = nouveau_canal
        self.date_modification = datetime.utcnow()

    def peut_se_connecter(self) -> bool:
        """Vérifie si l'utilisateur peut se connecter."""
        return self.statut.is_active

    @property
    def nom_complet(self) -> str:
        """Retourne le nom complet de l'utilisateur."""
        return f"{self.prenom} {self.nom}"