"""Schemas Pydantic pour les candidatures (côté RH)."""

from pydantic import BaseModel, Field
from typing import Optional, List

from ....domain.enums import (
    Disponibilite,
    NiveauAcademique,
    Sexe,
    StatutCandidature,
    TypeOffre,
)
from .candidat_schemas import CandidatureResponse


class ChangerStatutRequest(BaseModel):
    """Schema de requête pour changer le statut d'une candidature."""

    nouveau_statut: StatutCandidature = Field(..., description="Nouveau statut de la candidature")
    commentaire: Optional[str] = Field(None, description="Commentaire sur le changement de statut")

    class Config:
        json_schema_extra = {
            "example": {
                "nouveau_statut": "PRESELECTIONNEE",
                "commentaire": "Profil intéressant, à convoquer pour entretien"
            }
        }


class AjouterNotesRequest(BaseModel):
    """Schema de requête pour ajouter des notes internes."""

    notes: str = Field(..., min_length=10, description="Notes internes sur la candidature")

    class Config:
        json_schema_extra = {
            "example": {
                "notes": "Candidat avec une bonne expérience en développement Python. Formation solide. À considérer pour la suite du processus."
            }
        }


class RechercherCandidaturesRequest(BaseModel):
    """Schema de requête pour la recherche multicritère de candidatures."""

    texte: Optional[str] = Field(None, description="Recherche textuelle libre")
    statut: Optional[StatutCandidature] = Field(None, description="Filtrer par statut")
    offre_id: Optional[str] = Field(None, description="Filtrer par offre spécifique")
    candidat_nom: Optional[str] = Field(None, description="Rechercher par nom de candidat")
    date_debut: Optional[str] = Field(None, description="Date de début (ISO format)")
    date_fin: Optional[str] = Field(None, description="Date de fin (ISO format)")
    spontanee: Optional[bool] = Field(None, description="Filtrer les candidatures spontanées")
    # Critères du profil candidat
    sexe: Optional[Sexe] = Field(None, description="Filtrer par sexe du candidat")
    age_min: Optional[int] = Field(None, ge=14, le=100, description="Âge minimum (calculé depuis la date de naissance)")
    age_max: Optional[int] = Field(None, ge=14, le=100, description="Âge maximum (calculé depuis la date de naissance)")
    diplome: Optional[str] = Field(None, description="Diplôme (mappé sur le niveau académique)")
    domaine_formation: Optional[str] = Field(None, description="Domaine de formation")
    niveau_academique: Optional[NiveauAcademique] = Field(None, description="Niveau académique")
    specialite: Optional[str] = Field(None, description="Spécialité")
    competences: Optional[List[str]] = Field(None, description="Compétences requises")
    region_origine: Optional[str] = Field(None, description="Région d'origine")
    region_residence: Optional[str] = Field(None, description="Région de résidence")
    langues_parlees: Optional[List[str]] = Field(None, description="Langues parlées")
    disponibilite: Optional[Disponibilite] = Field(None, description="Disponibilité")
    type_offre: Optional[TypeOffre] = Field(None, description="Type d'offre (EMPLOI/STAGE)")
    # Pagination
    page: int = Field(1, ge=1, description="Numéro de page")
    taille_page: int = Field(20, ge=1, le=100, description="Nombre d'éléments par page")

    class Config:
        json_schema_extra = {
            "example": {
                "texte": "développeur",
                "sexe": "MASCULIN",
                "niveau_academique": "MASTER",
                "region_residence": "Dakar",
                "disponibilite": "IMMEDIATE",
                "type_offre": "EMPLOI",
                "page": 1,
                "taille_page": 20
            }
        }


class CandidaturesListResponse(BaseModel):
    """Schema de réponse pour la liste de candidatures."""

    candidatures: List[CandidatureResponse]
    total: int
    page: int
    taille_page: int
    pages_total: int

    class Config:
        from_attributes = True