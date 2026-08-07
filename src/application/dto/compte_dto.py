"""DTOs pour la gestion des comptes utilisateur."""

from dataclasses import dataclass
from typing import Optional

from ...domain.enums import CanalNotification, StatutCompte


@dataclass
class CreerCompteDTO:
    """DTO pour la création d'un compte utilisateur."""

    email: str
    telephone: Optional[str]
    mot_de_passe: str
    nom: str
    prenom: str
    canal_validation: CanalNotification


@dataclass
class ValiderCompteDTO:
    """DTO pour la validation d'un compte utilisateur."""

    email: str
    code_validation: str


@dataclass
class AuthentificationDTO:
    """DTO pour l'authentification d'un utilisateur."""

    email: str
    mot_de_passe: str


@dataclass
class ModifierCanalNotificationDTO:
    """DTO pour la modification du canal de notification."""

    utilisateur_id: str  # UUID en string
    nouveau_canal: CanalNotification


@dataclass
class UtilisateurDTO:
    """DTO de sortie pour les informations utilisateur."""

    id: str
    email: str
    telephone: Optional[str]
    nom: str
    prenom: str
    nom_complet: str
    statut: StatutCompte
    canal_validation: CanalNotification
    email_verifie: bool
    telephone_verifie: bool
    date_creation: str  # ISO format
    date_derniere_connexion: Optional[str] = None
    photo_url: Optional[str] = None  # Seulement pour les candidats


@dataclass
class TokenDTO:
    """DTO pour les jetons d'authentification."""

    access_token: str
    token_type: str
    expires_in: int
    utilisateur: UtilisateurDTO