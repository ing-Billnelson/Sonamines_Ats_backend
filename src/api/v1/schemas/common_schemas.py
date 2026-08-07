"""Schemas Pydantic communs."""

from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional


class ErrorResponse(BaseModel):
    """Schema de réponse pour les erreurs."""

    error: str = Field(..., description="Type d'erreur")
    message: str = Field(..., description="Message d'erreur détaillé")
    details: Optional[Dict[str, Any]] = Field(None, description="Détails supplémentaires sur l'erreur")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "ValidationError",
                "message": "Les données fournies sont invalides",
                "details": {
                    "field": "email",
                    "reason": "Format d'email invalide"
                }
            }
        }


class SuccessResponse(BaseModel):
    """Schema de réponse pour les opérations réussies."""

    success: bool = True
    message: str = Field(..., description="Message de succès")
    data: Optional[Dict[str, Any]] = Field(None, description="Données supplémentaires")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Opération réalisée avec succès",
                "data": {"id": "123e4567-e89b-12d3-a456-426614174000"}
            }
        }


class PaginationResponse(BaseModel):
    """Schema de base pour les réponses paginées."""

    total: int = Field(..., description="Nombre total d'éléments")
    page: int = Field(..., description="Page courante")
    taille_page: int = Field(..., description="Nombre d'éléments par page")
    pages_total: int = Field(..., description="Nombre total de pages")

    class Config:
        json_schema_extra = {
            "example": {
                "total": 150,
                "page": 2,
                "taille_page": 20,
                "pages_total": 8
            }
        }


class FileUploadResponse(BaseModel):
    """Schema de réponse pour les téléversements de fichiers."""

    id: str = Field(..., description="ID du fichier téléversé")
    nom_original: str = Field(..., description="Nom original du fichier")
    taille_octets: int = Field(..., description="Taille du fichier en octets")
    type_mime: str = Field(..., description="Type MIME du fichier")
    url_acces: Optional[str] = Field(None, description="URL d'accès temporaire au fichier")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "nom_original": "CV_Amadou_Diop.pdf",
                "taille_octets": 1048576,
                "type_mime": "application/pdf",
                "url_acces": "https://minio.example.com/documents/temp/cv.pdf"
            }
        }