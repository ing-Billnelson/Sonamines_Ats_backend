"""Schemas Pydantic pour les candidatures (côté RH)."""

from pydantic import BaseModel, Field
from typing import Optional, List

from ....domain.enums import StatutCandidature
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
    """Schema de requête pour la recherche de candidatures."""

    texte: Optional[str] = Field(None, description="Recherche textuelle libre")
    statut: Optional[StatutCandidature] = Field(None, description="Filtrer par statut")
    offre_id: Optional[str] = Field(None, description="Filtrer par offre spécifique")
    candidat_nom: Optional[str] = Field(None, description="Rechercher par nom de candidat")
    date_debut: Optional[str] = Field(None, description="Date de début (ISO format)")
    date_fin: Optional[str] = Field(None, description="Date de fin (ISO format)")
    spontanee: Optional[bool] = Field(None, description="Filtrer les candidatures spontanées")
    page: int = Field(1, ge=1, description="Numéro de page")
    taille_page: int = Field(20, ge=1, le=100, description="Nombre d'éléments par page")

    class Config:
        json_schema_extra = {
            "example": {
                "statut": "RECUE",
                "offre_id": "123e4567-e89b-12d3-a456-426614174000",
                "date_debut": "2024-01-01T00:00:00Z",
                "date_fin": "2024-01-31T23:59:59Z",
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