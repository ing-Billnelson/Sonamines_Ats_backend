"""Router pour l'administration RH et Super Admin."""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from ..schemas import (
    CreerCompteRequest,
    UtilisateurResponse,
    CreerOffreRequest,
    OffreResponse,
    OffresListResponse,
)
from ..dependencies import get_utilisateur_courant

router = APIRouter(prefix="/admin", tags=["Administration"])


# Routes Super Admin
@router.post(
    "/rh/comptes",
    response_model=UtilisateurResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Créer un compte Admin RH",
    description="Crée un nouveau compte administrateur RH (accès Super Admin)",
)
async def creer_compte_admin_rh(
    donnees: CreerCompteRequest,
    utilisateur_courant = Depends(get_utilisateur_courant),
):
    """Crée un compte administrateur RH."""
    # TODO: Vérifier les droits Super Admin
    # TODO: Implémenter la création de compte Admin RH
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail={"error": "NotImplemented", "message": "Endpoint en cours d'implémentation"},
    )


# Routes Admin RH
@router.post(
    "/offres",
    response_model=OffreResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Créer une offre",
    description="Crée une nouvelle offre d'emploi ou de stage (accès Admin RH)",
)
async def creer_offre(
    donnees: CreerOffreRequest,
    utilisateur_courant = Depends(get_utilisateur_courant),
):
    """Crée une nouvelle offre."""
    # TODO: Vérifier les droits Admin RH
    # TODO: Implémenter la création d'offre
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail={"error": "NotImplemented", "message": "Endpoint en cours d'implémentation"},
    )


@router.get(
    "/offres",
    response_model=OffresListResponse,
    summary="Lister mes offres",
    description="Liste toutes les offres créées par l'admin RH connecté",
)
async def lister_mes_offres(
    utilisateur_courant = Depends(get_utilisateur_courant),
):
    """Liste les offres créées par l'admin RH."""
    # TODO: Vérifier les droits Admin RH
    # TODO: Implémenter le listage des offres
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail={"error": "NotImplemented", "message": "Endpoint en cours d'implémentation"},
    )


@router.patch(
    "/offres/{offre_id}/publier",
    response_model=OffreResponse,
    summary="Publier une offre",
    description="Publie une offre (passe de BROUILLON à OUVERTE)",
)
async def publier_offre(
    offre_id: str,
    utilisateur_courant = Depends(get_utilisateur_courant),
):
    """Publie une offre."""
    # TODO: Vérifier les droits Admin RH
    # TODO: Implémenter la publication d'offre
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail={"error": "NotImplemented", "message": "Endpoint en cours d'implémentation"},
    )


@router.patch(
    "/offres/{offre_id}/cloturer",
    response_model=OffreResponse,
    summary="Clôturer une offre",
    description="Clôture une offre (passe de OUVERTE à CLOTUREE)",
)
async def cloturer_offre(
    offre_id: str,
    utilisateur_courant = Depends(get_utilisateur_courant),
):
    """Clôture une offre."""
    # TODO: Vérifier les droits Admin RH
    # TODO: Implémenter la clôture d'offre
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail={"error": "NotImplemented", "message": "Endpoint en cours d'implémentation"},
    )