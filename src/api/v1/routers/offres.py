"""Router pour les offres (public et RH)."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional

from ....application.use_cases import RechercherOffresUseCase
from ....application.dto import RechercherOffresDTO
from ....domain.enums import TypeOffre
from ....domain.exceptions import OffreIntrouvableError
from ..schemas import (
    CreerOffreRequest,
    OffreResponse,
    OffresListResponse,
    RechercherOffresRequest,
)
from ..dependencies import get_rechercher_offres_use_case

router = APIRouter(prefix="/offres", tags=["Offres"])


@router.get(
    "",
    response_model=OffresListResponse,
    summary="Lister les offres publiques",
    description="Liste les offres ouvertes aux candidatures avec possibilité de recherche",
)
async def lister_offres_publiques(
    texte: Optional[str] = Query(None, description="Recherche textuelle"),
    type_offre: Optional[TypeOffre] = Query(None, description="Type d'offre (EMPLOI/STAGE)"),
    lieu: Optional[str] = Query(None, description="Lieu de travail"),
    page: int = Query(1, ge=1, description="Numéro de page"),
    taille_page: int = Query(20, ge=1, le=100, description="Nombre d'éléments par page"),
    use_case: RechercherOffresUseCase = Depends(get_rechercher_offres_use_case),
):
    """Liste les offres publiques avec recherche."""
    dto = RechercherOffresDTO(
        texte=texte,
        type_offre=type_offre,
        lieu=lieu,
        limit=taille_page,
        offset=(page - 1) * taille_page,
    )

    offres_dto = await use_case.executer(dto)

    offres_response = [
        OffreResponse(
            id=offre.id,
            numero_reference=offre.numero_reference,
            titre=offre.titre,
            description=offre.description,
            type_offre=offre.type_offre,
            type_contrat=offre.type_contrat,
            type_stage=offre.type_stage,
            statut=offre.statut,
            lieu=offre.lieu,
            date_limite_candidature=offre.date_limite_candidature,
            salaire_min=offre.salaire_min,
            salaire_max=offre.salaire_max,
            competences_requises=offre.competences_requises,
            experience_requise=offre.experience_requise,
            createur_nom_complet=offre.createur_nom_complet,
            date_creation=offre.date_creation,
            date_publication=offre.date_publication,
            date_cloture=offre.date_cloture,
        )
        for offre in offres_dto
    ]

    total = len(offres_dto)
    pages_total = (total + taille_page - 1) // taille_page

    return OffresListResponse(
        offres=offres_response,
        total=total,
        page=page,
        taille_page=taille_page,
        pages_total=pages_total,
    )


@router.get(
    "/{offre_id}",
    response_model=OffreResponse,
    summary="Obtenir une offre",
    description="Récupère les détails d'une offre spécifique",
)
async def obtenir_offre(
    offre_id: str,
    use_case: RechercherOffresUseCase = Depends(get_rechercher_offres_use_case),
):
    """Récupère une offre par son ID."""
    try:
        offre_dto = await use_case.executer_par_id(offre_id)

        return OffreResponse(
            id=offre_dto.id,
            numero_reference=offre_dto.numero_reference,
            titre=offre_dto.titre,
            description=offre_dto.description,
            type_offre=offre_dto.type_offre,
            type_contrat=offre_dto.type_contrat,
            type_stage=offre_dto.type_stage,
            statut=offre_dto.statut,
            lieu=offre_dto.lieu,
            date_limite_candidature=offre_dto.date_limite_candidature,
            salaire_min=offre_dto.salaire_min,
            salaire_max=offre_dto.salaire_max,
            competences_requises=offre_dto.competences_requises,
            experience_requise=offre_dto.experience_requise,
            createur_nom_complet=offre_dto.createur_nom_complet,
            date_creation=offre_dto.date_creation,
            date_publication=offre_dto.date_publication,
            date_cloture=offre_dto.date_cloture,
        )

    except OffreIntrouvableError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "OffreIntrouvable", "message": str(e)},
        )