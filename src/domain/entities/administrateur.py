"""Entités administrateur."""

from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from ..enums import CanalNotification, StatutCompte
from ..value_objects import Email, NumeroTelephone
from .utilisateur import Utilisateur


@dataclass
class Administrateur(Utilisateur, ABC):
    """Entité abstraite représentant un administrateur du système."""

    pass


@dataclass
class SuperAdministrateur(Administrateur):
    """Entité représentant un super administrateur (peut créer des admins RH)."""

    @classmethod
    def creer_nouveau(
        cls,
        email: Email,
        telephone: Optional[NumeroTelephone],
        mot_de_passe_hash: str,
        nom: str,
        prenom: str,
        canal_validation: CanalNotification,
    ) -> "SuperAdministrateur":
        """Crée un nouveau super administrateur avec les valeurs par défaut."""
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


@dataclass
class AdministrateurRH(Administrateur):
    """Entité représentant un administrateur RH (gère les offres et candidatures)."""

    @classmethod
    def creer_nouveau(
        cls,
        email: Email,
        telephone: Optional[NumeroTelephone],
        mot_de_passe_hash: str,
        nom: str,
        prenom: str,
        canal_validation: CanalNotification,
    ) -> "AdministrateurRH":
        """Crée un nouveau administrateur RH avec les valeurs par défaut."""
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