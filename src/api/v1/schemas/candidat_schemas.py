"""Schemas Pydantic pour les candidats."""

from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

from ....domain.entities.document import TypeDocument
from ....domain.enums import (
    Disponibilite,
    NiveauAcademique,
    Sexe,
    StatutCandidature,
)


class ModifierProfilRequest(BaseModel):
    """Schema de requête pour modifier le profil candidat."""

    nom: Optional[str] = Field(None, min_length=2, max_length=100, description="Nom de famille")
    prenom: Optional[str] = Field(None, min_length=2, max_length=100, description="Prénom")
    telephone: Optional[str] = Field(None, description="Numéro de téléphone")
    linkedin_url: Optional[str] = Field(None, description="URL du profil LinkedIn")
    adresse: Optional[str] = Field(None, description="Adresse du candidat")
    competences: Optional[List[str]] = Field(None, description="Compétences du candidat")
    sexe: Optional[Sexe] = Field(None, description="Sexe du candidat")
    date_naissance: Optional[datetime] = Field(None, description="Date de naissance du candidat")
    nationalite: Optional[str] = Field(None, description="Nationalité du candidat")
    region_origine: Optional[str] = Field(None, description="Région d'origine du candidat")
    region_residence: Optional[str] = Field(None, description="Région de résidence du candidat")
    langues_parlees: Optional[List[str]] = Field(None, description="Langues parlées par le candidat")
    disponibilite: Optional[Disponibilite] = Field(None, description="Disponibilité du candidat")
    niveau_academique: Optional[NiveauAcademique] = Field(None, description="Niveau académique du candidat")
    domaine_formation: Optional[str] = Field(None, description="Domaine de formation du candidat")
    specialite: Optional[str] = Field(None, description="Spécialité du candidat")

    class Config:
        json_schema_extra = {
            "example": {
                "nom": "Diop",
                "prenom": "Amadou",
                "telephone": "+221771234567",
                "linkedin_url": "https://linkedin.com/in/amadou",
                "adresse": "Dakar, Sénégal",
                "competences": ["Python", "SQL"],
                "sexe": "MASCULIN",
                "date_naissance": "1990-05-12",
                "nationalite": "Sénégalaise",
                "region_origine": "Diourbel",
                "region_residence": "Dakar",
                "langues_parlees": ["Français", "Wolof"],
                "disponibilite": "IMMEDIATE",
                "niveau_academique": "MASTER",
                "domaine_formation": "Informatique",
                "specialite": "Développement Backend"
            }
        }


class FormationResponse(BaseModel):
    """Schema de réponse pour une formation."""

    id: str
    etablissement: str
    diplome: str
    annee_debut: int
    annee_fin: Optional[int] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "etablissement": "Université Cheikh Anta Diop",
                "diplome": "Master en Informatique",
                "annee_debut": 2018,
                "annee_fin": 2020
            }
        }


class AjouterFormationRequest(BaseModel):
    """Schema de requête pour ajouter une formation."""

    etablissement: str = Field(..., min_length=2, max_length=255, description="Établissement")
    diplome: str = Field(..., min_length=2, max_length=255, description="Diplôme obtenu")
    annee_debut: int = Field(..., description="Année de début")
    annee_fin: Optional[int] = Field(None, description="Année de fin")

    class Config:
        json_schema_extra = {
            "example": {
                "etablissement": "Université Cheikh Anta Diop",
                "diplome": "Master en Informatique",
                "annee_debut": 2018,
                "annee_fin": 2020
            }
        }


class ExperienceResponse(BaseModel):
    """Schema de réponse pour une expérience professionnelle."""

    id: str
    entreprise: str
    poste: str
    date_debut: str
    date_fin: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "entreprise": "SONAMINES SA",
                "poste": "Développeur Backend",
                "date_debut": "2021-01-15T00:00:00",
                "date_fin": "2023-06-30T00:00:00",
                "description": "Développement d'APIs REST"
            }
        }


class AjouterExperienceRequest(BaseModel):
    """Schema de requête pour ajouter une expérience professionnelle."""

    entreprise: str = Field(..., min_length=2, max_length=255, description="Entreprise")
    poste: str = Field(..., min_length=2, max_length=255, description="Poste occupé")
    date_debut: str = Field(..., description="Date de début (ISO)")
    date_fin: Optional[str] = Field(None, description="Date de fin (ISO)")
    description: Optional[str] = Field(None, description="Description")

    class Config:
        json_schema_extra = {
            "example": {
                "entreprise": "SONAMINES SA",
                "poste": "Développeur Backend",
                "date_debut": "2021-01-15",
                "date_fin": "2023-06-30",
                "description": "Développement d'APIs REST"
            }
        }


class SoumettreKandidatureRequest(BaseModel):
    """Schema de requête pour soumettre une candidature."""

    message_motivation: Optional[str] = Field(None, description="Message de motivation (optionnel)")
    offre_id: Optional[str] = Field(None, description="ID de l'offre (None pour candidature spontanée)")

    class Config:
        json_schema_extra = {
            "example": {
                "message_motivation": "Je suis très intéressé par ce poste car il correspond parfaitement à mon profil et à mes aspirations professionnelles...",
                "offre_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        }


class DocumentResponse(BaseModel):
    """Schema de réponse pour un document."""

    id: str
    type_document: TypeDocument
    nom_original: str
    taille_octets: int
    type_mime: str
    url_temporaire: Optional[str]
    date_telechargement: str
    telechargeur_nom_complet: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "type_document": "CV",
                "nom_original": "CV_Amadou_Diop.pdf",
                "taille_octets": 1048576,
                "type_mime": "application/pdf",
                "url_temporaire": "https://minio.example.com/documents/temp/cv.pdf?expires=3600",
                "date_telechargement": "2024-01-15T10:30:00Z",
                "telechargeur_nom_complet": "Amadou Diop"
            }
        }


class HistoriqueStatutResponse(BaseModel):
    """Schema de réponse pour l'historique des statuts."""

    id: str
    ancien_statut: Optional[StatutCandidature]
    nouveau_statut: StatutCandidature
    commentaire: Optional[str]
    utilisateur_nom_complet: str
    date_changement: str

    class Config:
        from_attributes = True


class CandidatureResponse(BaseModel):
    """Schema de réponse pour une candidature."""

    id: str
    numero_reference: str
    candidat_nom_complet: str
    candidat_email: str
    offre_titre: Optional[str]
    offre_numero_reference: Optional[str]
    statut: StatutCandidature
    message_motivation: Optional[str] = None
    notes_internes: Optional[str]
    date_soumission: str
    date_derniere_modification: str
    documents: List[DocumentResponse]
    historique: List[HistoriqueStatutResponse]
    est_spontanee: bool
    est_complete: bool

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "numero_reference": "CAND-2024-ABC12345",
                "candidat_nom_complet": "Amadou Diop",
                "candidat_email": "amadou.diop@example.com",
                "offre_titre": "Ingénieur Logiciel Senior",
                "offre_numero_reference": "EMPLOI-2024-XYZ67890",
                "statut": "RECUE",
                "message_motivation": "Je suis très intéressé par ce poste...",
                "notes_internes": None,
                "date_soumission": "2024-01-15T10:30:00Z",
                "date_derniere_modification": "2024-01-15T10:30:00Z",
                "documents": [],
                "historique": [],
                "est_spontanee": False,
                "est_complete": True
            }
        }


class TeleverserDocumentRequest(BaseModel):
    """Schema pour les métadonnées de téléversement de document."""

    type_document: TypeDocument = Field(..., description="Type de document")

    class Config:
        json_schema_extra = {
            "example": {
                "type_document": "CV"
            }
        }