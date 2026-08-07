"""Schemas Pydantic pour les offres."""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from ....domain.entities.offre import StatutOffre
from ....domain.enums import TypeContrat, TypeOffre, TypeStage


class CreerOffreRequest(BaseModel):
    """Schema de requête pour créer une offre."""

    titre: str = Field(..., min_length=5, max_length=200, description="Titre de l'offre")
    description: str = Field(..., min_length=50, description="Description détaillée de l'offre")
    type_offre: TypeOffre = Field(..., description="Type d'offre (EMPLOI ou STAGE)")
    type_contrat: Optional[TypeContrat] = Field(None, description="Type de contrat (requis pour les emplois)")
    type_stage: Optional[TypeStage] = Field(None, description="Type de stage (requis pour les stages)")
    lieu: str = Field(..., min_length=2, max_length=100, description="Lieu de travail")
    date_limite_candidature: Optional[str] = Field(None, description="Date limite de candidature (ISO format)")
    salaire_min: Optional[float] = Field(None, ge=0, description="Salaire minimum")
    salaire_max: Optional[float] = Field(None, ge=0, description="Salaire maximum")
    competences_requises: List[str] = Field(default_factory=list, description="Liste des compétences requises")
    experience_requise: Optional[str] = Field(None, description="Expérience requise")

    class Config:
        json_schema_extra = {
            "example": {
                "titre": "Ingénieur Logiciel Senior",
                "description": "Nous recherchons un ingénieur logiciel senior pour rejoindre notre équipe de développement...",
                "type_offre": "EMPLOI",
                "type_contrat": "CDI",
                "type_stage": None,
                "lieu": "Dakar, Sénégal",
                "date_limite_candidature": "2024-02-28T23:59:59Z",
                "salaire_min": 800000,
                "salaire_max": 1200000,
                "competences_requises": ["Python", "FastAPI", "PostgreSQL", "Docker"],
                "experience_requise": "5 ans minimum en développement web"
            }
        }


class OffreResponse(BaseModel):
    """Schema de réponse pour une offre."""

    id: str
    numero_reference: str
    titre: str
    description: str
    type_offre: TypeOffre
    type_contrat: Optional[TypeContrat]
    type_stage: Optional[TypeStage]
    statut: StatutOffre
    lieu: str
    date_limite_candidature: Optional[str]
    salaire_min: Optional[float]
    salaire_max: Optional[float]
    competences_requises: List[str]
    experience_requise: Optional[str]
    createur_nom_complet: str
    date_creation: str
    date_publication: Optional[str]
    date_cloture: Optional[str]
    nombre_candidatures: Optional[int] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "numero_reference": "EMPLOI-2024-XYZ67890",
                "titre": "Ingénieur Logiciel Senior",
                "description": "Nous recherchons un ingénieur logiciel senior...",
                "type_offre": "EMPLOI",
                "type_contrat": "CDI",
                "type_stage": None,
                "statut": "OUVERTE",
                "lieu": "Dakar, Sénégal",
                "date_limite_candidature": "2024-02-28T23:59:59Z",
                "salaire_min": 800000,
                "salaire_max": 1200000,
                "competences_requises": ["Python", "FastAPI", "PostgreSQL"],
                "experience_requise": "5 ans minimum",
                "createur_nom_complet": "Marie Dupont",
                "date_creation": "2024-01-15T10:30:00Z",
                "date_publication": "2024-01-15T14:00:00Z",
                "date_cloture": None,
                "nombre_candidatures": 15
            }
        }


class RechercherOffresRequest(BaseModel):
    """Schema de requête pour la recherche d'offres."""

    texte: Optional[str] = Field(None, description="Recherche textuelle libre")
    type_offre: Optional[TypeOffre] = Field(None, description="Filtrer par type d'offre")
    type_contrat: Optional[TypeContrat] = Field(None, description="Filtrer par type de contrat")
    type_stage: Optional[TypeStage] = Field(None, description="Filtrer par type de stage")
    lieu: Optional[str] = Field(None, description="Filtrer par lieu")
    competences: List[str] = Field(default_factory=list, description="Filtrer par compétences")
    salaire_min: Optional[float] = Field(None, ge=0, description="Salaire minimum souhaité")
    salaire_max: Optional[float] = Field(None, ge=0, description="Salaire maximum souhaité")
    page: int = Field(1, ge=1, description="Numéro de page")
    taille_page: int = Field(20, ge=1, le=100, description="Nombre d'éléments par page")

    class Config:
        json_schema_extra = {
            "example": {
                "texte": "développeur python",
                "type_offre": "EMPLOI",
                "lieu": "Dakar",
                "competences": ["Python", "FastAPI"],
                "salaire_min": 500000,
                "page": 1,
                "taille_page": 20
            }
        }


class OffresListResponse(BaseModel):
    """Schema de réponse pour la liste d'offres."""

    offres: List[OffreResponse]
    total: int
    page: int
    taille_page: int
    pages_total: int

    class Config:
        from_attributes = True