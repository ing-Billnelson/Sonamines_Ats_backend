"""Router pour la gestion des candidatures (côté RH)."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional

from ....application.use_cases import (
    ListerCandidaturesRHUseCase,
    ChangerStatutCandidatureUseCase,
    RechercherCandidaturesUseCase,
    ObtenirCandidatureRHUseCase,
    AjouterNotesInternesUseCase,
)
from ....application.dto import UtilisateurDTO, RechercherCandidaturesDTO
from ....domain.enums import StatutCandidature
from ....domain.exceptions import (
    CandidatureIntrouvableError,
    RechercheIndisponibleError,
    UtilisateurIntrouvableError,
)
from ..schemas import (
    CandidaturesListResponse,
    CandidatureResponse,
    ChangerStatutRequest,
    AjouterNotesRequest,
    RechercherCandidaturesRequest,
)
from ..dependencies import (
    get_admin_rh_courant,
    get_lister_candidatures_rh_use_case,
    get_changer_statut_candidature_use_case,
    get_rechercher_candidatures_use_case,
    get_obtenir_candidature_rh_use_case,
    get_ajouter_notes_internes_use_case,
)

router = APIRouter(prefix="/candidatures", tags=["Gestion des candidatures (RH)"])


@router.get(
    "",
    response_model=CandidaturesListResponse,
    summary="Lister les candidatures (RH)",
    description="Liste toutes les candidatures avec filtres et recherche (accès RH)",
)
async def lister_candidatures_rh(
    statut: Optional[StatutCandidature] = Query(None, description="Filtrer par statut"),
    offre_id: Optional[str] = Query(None, description="Filtrer par offre"),
    spontanee: Optional[bool] = Query(None, description="Candidatures spontanées uniquement"),
    page: int = Query(1, ge=1, description="Numéro de page"),
    taille_page: int = Query(20, ge=1, le=100, description="Nombre d'éléments par page"),
    utilisateur_courant = Depends(get_admin_rh_courant),
    use_case: ListerCandidaturesRHUseCase = Depends(get_lister_candidatures_rh_use_case),
):
    """Liste les candidatures (accès RH)."""
    candidatures, total = await use_case.executer(
        statut=statut,
        offre_id=offre_id,
        spontanee=spontanee,
        page=page,
        taille_page=taille_page,
    )

    pages_total = (total + taille_page - 1) // taille_page

    return CandidaturesListResponse(
        candidatures=[
            CandidatureResponse(
                id=c.id,
                numero_reference=c.numero_reference,
                candidat_nom_complet=c.candidat_nom_complet,
                candidat_email=c.candidat_email,
                offre_titre=c.offre_titre,
                offre_numero_reference=c.offre_numero_reference,
                statut=c.statut,
                message_motivation=c.message_motivation,
                notes_internes=c.notes_internes,
                date_soumission=c.date_soumission,
                date_derniere_modification=c.date_derniere_modification,
                documents=c.documents,
                historique=c.historique,
                est_spontanee=c.est_spontanee,
                est_complete=c.est_complete,
            )
            for c in candidatures
        ],
        total=total,
        page=page,
        taille_page=taille_page,
        pages_total=pages_total,
    )


@router.post(
    "/recherche",
    response_model=CandidaturesListResponse,
    summary="Recherche multicritère de candidatures (RH)",
    description="Recherche des candidatures avec des filtres multiples issus du profil candidat (accès RH)",
)
async def rechercher_candidatures_rh(
    donnees: RechercherCandidaturesRequest,
    utilisateur_courant = Depends(get_admin_rh_courant),
    use_case: RechercherCandidaturesUseCase = Depends(get_rechercher_candidatures_use_case),
):
    """Recherche multicritère de candidatures."""
    try:
        dto = RechercherCandidaturesDTO(
            texte=donnees.texte,
            statut=donnees.statut,
            offre_id=donnees.offre_id,
            candidat_nom=donnees.candidat_nom,
            date_debut=donnees.date_debut,
            date_fin=donnees.date_fin,
            spontanee=donnees.spontanee,
            sexe=donnees.sexe,
            age_min=donnees.age_min,
            age_max=donnees.age_max,
            diplome=donnees.diplome,
            domaine_formation=donnees.domaine_formation,
            niveau_academique=donnees.niveau_academique,
            specialite=donnees.specialite,
            competences=donnees.competences,
            region_origine=donnees.region_origine,
            region_residence=donnees.region_residence,
            langues_parlees=donnees.langues_parlees,
            disponibilite=donnees.disponibilite,
            type_offre=donnees.type_offre,
            limit=donnees.taille_page,
            offset=(donnees.page - 1) * donnees.taille_page,
        )

        candidatures, total = await use_case.executer(dto)
    except RechercheIndisponibleError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"error": "RechercheIndisponible", "message": str(e)},
        )

    pages_total = (total + donnees.taille_page - 1) // donnees.taille_page

    return CandidaturesListResponse(
        candidatures=[
            CandidatureResponse(
                id=c.id,
                numero_reference=c.numero_reference,
                candidat_nom_complet=c.candidat_nom_complet,
                candidat_email=c.candidat_email,
                offre_titre=c.offre_titre,
                offre_numero_reference=c.offre_numero_reference,
                statut=c.statut,
                message_motivation=c.message_motivation,
                notes_internes=c.notes_internes,
                date_soumission=c.date_soumission,
                date_derniere_modification=c.date_derniere_modification,
                documents=c.documents,
                historique=c.historique,
                est_spontanee=c.est_spontanee,
                est_complete=c.est_complete,
            )
            for c in candidatures
        ],
        total=total,
        page=donnees.page,
        taille_page=donnees.taille_page,
        pages_total=pages_total,
    )


@router.get(
    "/{candidature_id}",
    response_model=CandidatureResponse,
    summary="Obtenir une candidature (RH)",
    description="Récupère les détails complets d'une candidature (accès RH)",
)
async def obtenir_candidature_rh(
    candidature_id: str,
    utilisateur_courant = Depends(get_admin_rh_courant),
    use_case: ObtenirCandidatureRHUseCase = Depends(get_obtenir_candidature_rh_use_case),
):
    """Récupère une candidature complète (accès RH)."""
    try:
        candidature_dto = await use_case.executer(candidature_id=candidature_id)
    except CandidatureIntrouvableError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "CandidatureIntrouvable", "message": str(e)},
        )

    return CandidatureResponse(
        id=candidature_dto.id,
        numero_reference=candidature_dto.numero_reference,
        candidat_nom_complet=candidature_dto.candidat_nom_complet,
        candidat_email=candidature_dto.candidat_email,
        offre_titre=candidature_dto.offre_titre,
        offre_numero_reference=candidature_dto.offre_numero_reference,
        statut=candidature_dto.statut,
        message_motivation=candidature_dto.message_motivation,
        notes_internes=candidature_dto.notes_internes,
        date_soumission=candidature_dto.date_soumission,
        date_derniere_modification=candidature_dto.date_derniere_modification,
        documents=candidature_dto.documents,
        historique=candidature_dto.historique,
        est_spontanee=candidature_dto.est_spontanee,
        est_complete=candidature_dto.est_complete,
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
    utilisateur_courant: UtilisateurDTO = Depends(get_admin_rh_courant),
    use_case: ChangerStatutCandidatureUseCase = Depends(get_changer_statut_candidature_use_case),
):
    """Change le statut d'une candidature."""
    try:
        candidature_dto = await use_case.executer(
            candidature_id=candidature_id,
            nouveau_statut=donnees.nouveau_statut,
            commentaire=donnees.commentaire,
            utilisateur_id=utilisateur_courant.id,
        )
    except CandidatureIntrouvableError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "CandidatureIntrouvable", "message": str(e)},
        )
    except UtilisateurIntrouvableError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "UtilisateurIntrouvable", "message": str(e)},
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error": "TransitionInvalide", "message": str(e)},
        )

    return CandidatureResponse(
        id=candidature_dto.id,
        numero_reference=candidature_dto.numero_reference,
        candidat_nom_complet=candidature_dto.candidat_nom_complet,
        candidat_email=candidature_dto.candidat_email,
        offre_titre=candidature_dto.offre_titre,
        offre_numero_reference=candidature_dto.offre_numero_reference,
        statut=candidature_dto.statut,
        message_motivation=candidature_dto.message_motivation,
        notes_internes=candidature_dto.notes_internes,
        date_soumission=candidature_dto.date_soumission,
        date_derniere_modification=candidature_dto.date_derniere_modification,
        documents=candidature_dto.documents,
        historique=candidature_dto.historique,
        est_spontanee=candidature_dto.est_spontanee,
        est_complete=candidature_dto.est_complete,
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
    utilisateur_courant = Depends(get_admin_rh_courant),
    use_case: AjouterNotesInternesUseCase = Depends(get_ajouter_notes_internes_use_case),
):
    """Ajoute des notes internes à une candidature (accès RH)."""
    try:
        candidature_dto = await use_case.executer(
            candidature_id=candidature_id,
            notes=donnees.notes,
        )
    except CandidatureIntrouvableError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "CandidatureIntrouvable", "message": str(e)},
        )

    return CandidatureResponse(
        id=candidature_dto.id,
        numero_reference=candidature_dto.numero_reference,
        candidat_nom_complet=candidature_dto.candidat_nom_complet,
        candidat_email=candidature_dto.candidat_email,
        offre_titre=candidature_dto.offre_titre,
        offre_numero_reference=candidature_dto.offre_numero_reference,
        statut=candidature_dto.statut,
        message_motivation=candidature_dto.message_motivation,
        notes_internes=candidature_dto.notes_internes,
        date_soumission=candidature_dto.date_soumission,
        date_derniere_modification=candidature_dto.date_derniere_modification,
        documents=candidature_dto.documents,
        historique=candidature_dto.historique,
        est_spontanee=candidature_dto.est_spontanee,
        est_complete=candidature_dto.est_complete,
    )