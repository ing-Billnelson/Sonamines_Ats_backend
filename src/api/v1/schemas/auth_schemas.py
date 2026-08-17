"""Schemas Pydantic pour l'authentification."""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional

from ....domain.enums import CanalNotification, StatutCompte


class CreerCompteRequest(BaseModel):
    """Schema de requête pour la création de compte."""

    email: EmailStr
    telephone: Optional[str] = Field(None, description="Numéro de téléphone (optionnel)")
    mot_de_passe: str = Field(..., min_length=8, description="Mot de passe (minimum 8 caractères)")
    nom: str = Field(..., min_length=2, max_length=100, description="Nom de famille")
    prenom: str = Field(..., min_length=2, max_length=100, description="Prénom")
    canal_validation: CanalNotification = Field(..., description="Canal de validation souhaité")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "candidat@example.com",
                "telephone": "+221771234567",
                "mot_de_passe": "motdepasse123",
                "nom": "Diop",
                "prenom": "Amadou",
                "canal_validation": "EMAIL"
            }
        }


class ValiderCompteRequest(BaseModel):
    """Schema de requête pour la validation de compte."""

    email: EmailStr
    code_validation: str = Field(..., min_length=6, max_length=10, description="Code de validation reçu")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "candidat@example.com",
                "code_validation": "123456"
            }
        }


class ConnexionRequest(BaseModel):
    """Schema de requête pour la connexion."""

    email: EmailStr
    mot_de_passe: str = Field(..., description="Mot de passe")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "candidat@example.com",
                "mot_de_passe": "motdepasse123"
            }
        }


class MotDePasseOublieRequest(BaseModel):
    """Schema de requête pour demander un code de réinitialisation de mot de passe."""

    email: EmailStr

    class Config:
        json_schema_extra = {
            "example": {
                "email": "candidat@example.com"
            }
        }


class ReinitialiserMotDePasseRequest(BaseModel):
    """Schema de requête pour réinitialiser le mot de passe avec un code."""

    email: EmailStr
    code_reinitialisation: str = Field(..., min_length=6, max_length=10, description="Code de réinitialisation reçu")
    nouveau_mot_de_passe: str = Field(..., min_length=8, description="Nouveau mot de passe (minimum 8 caractères)")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "candidat@example.com",
                "code_reinitialisation": "123456",
                "nouveau_mot_de_passe": "nouveaumotdepasse123"
            }
        }


class UtilisateurResponse(BaseModel):
    """Schema de réponse pour les informations utilisateur."""

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
    date_creation: str
    date_derniere_connexion: Optional[str] = None
    photo_url: Optional[str] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "candidat@example.com",
                "telephone": "+221771234567",
                "nom": "Diop",
                "prenom": "Amadou",
                "nom_complet": "Amadou Diop",
                "statut": "ACTIF",
                "canal_validation": "EMAIL",
                "email_verifie": True,
                "telephone_verifie": False,
                "date_creation": "2024-01-15T10:30:00Z",
                "date_derniere_connexion": "2024-01-15T14:20:00Z",
                "photo_url": None
            }
        }


class TokenResponse(BaseModel):
    """Schema de réponse pour les tokens d'authentification."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int
    utilisateur: UtilisateurResponse

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 1800,
                "utilisateur": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "email": "candidat@example.com",
                    "nom_complet": "Amadou Diop",
                    "statut": "ACTIF"
                }
            }
        }