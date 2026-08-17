"""Entité utilisateur abstraite."""

import secrets
from abc import ABC
from dataclasses import dataclass
from datetime import datetime, timedelta
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
    code_validation: Optional[str] = None
    code_validation_expiration: Optional[datetime] = None
    code_reinitialisation: Optional[str] = None
    code_reinitialisation_expiration: Optional[datetime] = None

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

    def generer_code_validation(self) -> None:
        """Génère un code de validation numérique à 6 chiffres (valable 5 minutes)."""
        self.code_validation = f"{secrets.randbelow(1000000):06d}"
        self.code_validation_expiration = datetime.utcnow() + timedelta(minutes=5)

    def code_validation_est_valide(self, code: str) -> bool:
        """Vérifie si le code fourni correspond et n'est pas expiré."""
        if not self.code_validation or not self.code_validation_expiration:
            return False
        if self.code_validation != code:
            return False
        if datetime.utcnow() > self.code_validation_expiration:
            return False
        return True

    def generer_code_reinitialisation(self) -> None:
        """Génère un code de réinitialisation numérique à 6 chiffres (valable 5 minutes)."""
        self.code_reinitialisation = f"{secrets.randbelow(1000000):06d}"
        self.code_reinitialisation_expiration = datetime.utcnow() + timedelta(minutes=5)

    def code_reinitialisation_est_valide(self, code: str) -> bool:
        """Vérifie si le code de réinitialisation fourni correspond et n'est pas expiré."""
        if not self.code_reinitialisation or not self.code_reinitialisation_expiration:
            return False
        if self.code_reinitialisation != code:
            return False
        if datetime.utcnow() > self.code_reinitialisation_expiration:
            return False
        return True

    def reinitialiser_mot_de_passe(self, nouveau_hash: str) -> None:
        """Réinitialise le mot de passe et invalide le code de réinitialisation."""
        self.mot_de_passe_hash = nouveau_hash
        self.code_reinitialisation = None
        self.code_reinitialisation_expiration = None

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