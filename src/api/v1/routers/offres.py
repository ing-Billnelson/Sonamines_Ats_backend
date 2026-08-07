"""Router pour les offres (public et RH)."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional

from ..schemas import (
    CreerOffreRequest,
    OffreResponse,
    OffresListResponse,
    RechercherOffresRequest,
)
from ..dependencies import get_utilisateur_courant

router = APIRouter(prefix="/offres", tags=["Offres"])


@router.get(
    "",
    response_model=OffresListResponse,
    summary="Lister les offres publiques",
    description="Liste les offres ouvertes aux candidatures avec possibilité de recherche",
)
async def lister_offres_publiques(
    texte: Optional[str] = Query(None, description="Recherche textuelle"),
    type_offre: Optional[str] = Query(None, description="Type d'offre (EMPLOI/STAGE)"),
    lieu: Optional[str] = Query(None, description="Lieu de travail"),
    page: int = Query(1, ge=1, description="Numéro de page"),
    taille_page: int = Query(20, ge=1, le=100, description="Nombre d'éléments par page"),
):
    """Liste les offres publiques avec recherche."""
    # TODO: Implémenter la recherche d'offres
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail={"error": "NotImplemented", "message": "Endpoint en cours d'implémentation"},
    )


@router.get(
    "/{offre_id}",
    response_model=OffreResponse,
    summary="Obtenir une offre",
    description="Récupère les détails d'une offre spécifique",
)
async def obtenir_offre(offre_id: str):
    """Récupère une offre par son ID."""
    # TODO: Implémenter la récupération d'offre
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail={"error": "NotImplemented", "message": "Endpoint en cours d'implémentation"},
    )