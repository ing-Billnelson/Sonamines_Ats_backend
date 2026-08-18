"""DTOs pour la gestion des comptes utilisateur."""

from dataclasses import dataclass, field
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
class DemanderReinitialisationDTO:
    """DTO pour demander un code de réinitialisation du mot de passe."""

    email: str


@dataclass
class ReinitialiserMotDePasseDTO:
    """DTO pour réinitialiser le mot de passe avec un code."""

    email: str
    code_reinitialisation: str
    nouveau_mot_de_passe: str


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
    role: Optional[str] = None  # Type d'utilisateur: candidat, administrateur_rh, super_administrateur
    linkedin_url: Optional[str] = None  # Seulement pour les candidats
    adresse: Optional[str] = None  # Seulement pour les candidats
    competences: list[str] = field(default_factory=list)  # Seulement pour les candidats
    formations: list["FormationDTO"] = field(default_factory=list)  # Seulement pour les candidats
    experiences: list["ExperienceDTO"] = field(default_factory=list)  # Seulement pour les candidats


@dataclass
class TokenDTO:
    """DTO pour les jetons d'authentification."""

    access_token: str
    token_type: str
    expires_in: int
    utilisateur: UtilisateurDTO


@dataclass
class ModifierProfilDTO:
    """DTO pour la modification du profil candidat."""

    candidat_id: str
    nom: Optional[str] = None
    prenom: Optional[str] = None
    telephone: Optional[str] = None
    linkedin_url: Optional[str] = None
    adresse: Optional[str] = None
    competences: Optional[list[str]] = None


@dataclass
class FormationDTO:
    """DTO de sortie pour une formation."""

    id: str
    etablissement: str
    diplome: str
    annee_debut: int
    annee_fin: Optional[int] = None


@dataclass
class AjouterFormationDTO:
    """DTO pour ajouter une formation."""

    candidat_id: str
    etablissement: str
    diplome: str
    annee_debut: int
    annee_fin: Optional[int] = None


@dataclass
class ExperienceDTO:
    """DTO de sortie pour une expérience professionnelle."""

    id: str
    entreprise: str
    poste: str
    date_debut: str  # ISO format
    date_fin: Optional[str] = None  # ISO format
    description: Optional[str] = None


@dataclass
class AjouterExperienceDTO:
    """DTO pour ajouter une expérience professionnelle."""

    candidat_id: str
    entreprise: str
    poste: str
    date_debut: str  # ISO format
    date_fin: Optional[str] = None  # ISO format
    description: Optional[str] = None