"""Router pour la gestion des candidatures (côté RH)."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional

from ..schemas import (
    CandidaturesListResponse,
    CandidatureResponse,
    ChangerStatutRequest,
    AjouterNotesRequest,
)
from ..dependencies import get_utilisateur_courant

router = APIRouter(prefix="/candidatures", tags=["Gestion des candidatures (RH)"])


@router.get(
    "",
    response_model=CandidaturesListResponse,
    summary="Lister les candidatures (RH)",
    description="Liste toutes les candidatures avec filtres et recherche (accès RH)",
)
async def lister_candidatures_rh(
    statut: Optional[str] = Query(None, description="Filtrer par statut"),
    offre_id: Optional[str] = Query(None, description="Filtrer par offre"),
    spontanee: Optional[bool] = Query(None, description="Candidatures spontanées uniquement"),
    page: int = Query(1, ge=1, description="Numéro de page"),
    taille_page: int = Query(20, ge=1, le=100, description="Nombre d'éléments par page"),
    utilisateur_courant = Depends(get_utilisateur_courant),
):
    """Liste les candidatures (accès RH)."""
    # TODO: Vérifier les droits RH
    # TODO: Implémenter la recherche de candidatures
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail={"error": "NotImplemented", "message": "Endpoint en cours d'implémentation"},
    )


@router.get(
    "/{candidature_id}",
    response_model=CandidatureResponse,
    summary="Obtenir une candidature (RH)",
    description="Récupère les détails complets d'une candidature (accès RH)",
)
async def obtenir_candidature_rh(
    candidature_id: str,
    utilisateur_courant = Depends(get_utilisateur_courant),
):
    """Récupère une candidature (accès RH)."""
    # TODO: Vérifier les droits RH
    # TODO: Implémenter la récupération de candidature
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail={"error": "NotImplemented", "message": "Endpoint en cours d'implémentation"},
    )


@router.patch(
    "/{candidature_id}/statut",
    response_model=CandidatureResponse,
    summary="Changer le statut d'une candidature",
    description="Change le statut d'une candidature avec historisation (accès RH)",
)
async def changer_statut_candidature(
    candidature_id: str,
    donnees: ChangerStatutRequest,
    utilisateur_courant = Depends(get_utilisateur_courant),
):
    """Change le statut d'une candidature."""
    # TODO: Vérifier les droits RH
    # TODO: Implémenter le changement de statut
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail={"error": "NotImplemented", "message": "Endpoint en cours d'implémentation"},
    )


@router.patch(
    "/{candidature_id}/notes",
    response_model=CandidatureResponse,
    summary="Ajouter des notes internes",
    description="Ajoute des notes internes à une candidature (accès RH)",
)
async def ajouter_notes_internes(
    candidature_id: str,
    donnees: AjouterNotesRequest,
    utilisateur_courant = Depends(get_utilisateur_courant),
):
    """Ajoute des notes internes à une candidature."""
    # TODO: Vérifier les droits RH
    # TODO: Implémenter l'ajout de notes
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail={"error": "NotImplemented", "message": "Endpoint en cours d'implémentation"},
    )