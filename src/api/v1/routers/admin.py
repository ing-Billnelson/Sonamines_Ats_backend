"""Router pour l'administration RH et Super Admin."""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from ....application.use_cases import (
    CreerOffreUseCase,
    PublierOffreUseCase,
    CloturerOffreUseCase,
    CreerCompteAdministrateurRHUseCase,
)
from ....application.dto import CreerOffreDTO, CreerCompteDTO
from ....domain.exceptions import OffreIntrouvableError, UtilisateurExistantError
from ..schemas import (
    CreerCompteRequest,
    UtilisateurResponse,
    CreerOffreRequest,
    OffreResponse,
    OffresListResponse,
)
from ..dependencies import (
    get_admin_rh_courant,
    get_super_admin_courant,
    get_creer_offre_use_case,
    get_publier_offre_use_case,
    get_cloturer_offre_use_case,
    get_creer_compte_administrateur_rh_use_case,
)

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
    utilisateur_courant = Depends(get_super_admin_courant),
    use_case: CreerCompteAdministrateurRHUseCase = Depends(get_creer_compte_administrateur_rh_use_case),
):
    """Crée un compte administrateur RH (accès Super Admin uniquement)."""
    try:
        dto = CreerCompteDTO(
            email=donnees.email,
            telephone=donnees.telephone,
            mot_de_passe=donnees.mot_de_passe,
            nom=donnees.nom,
            prenom=donnees.prenom,
            canal_validation=donnees.canal_validation,
        )

        admin_dto = await use_case.executer(dto)

        return UtilisateurResponse(
            id=admin_dto.id,
            email=admin_dto.email,
            telephone=admin_dto.telephone,
            nom=admin_dto.nom,
            prenom=admin_dto.prenom,
            nom_complet=admin_dto.nom_complet,
            statut=admin_dto.statut,
            canal_validation=admin_dto.canal_validation,
            email_verifie=admin_dto.email_verifie,
            telephone_verifie=admin_dto.telephone_verifie,
            date_creation=admin_dto.date_creation,
            date_derniere_connexion=admin_dto.date_derniere_connexion,
            photo_url=admin_dto.photo_url,
        )

    except UtilisateurExistantError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error": "UtilisateurExistant", "message": str(e)},
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error": "ValidationError", "message": str(e)},
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
    utilisateur_courant = Depends(get_admin_rh_courant),
    use_case: CreerOffreUseCase = Depends(get_creer_offre_use_case),
):
    """Crée une nouvelle offre."""
    try:
        # Convertir le schema Pydantic en DTO de requête
        dto = CreerOffreDTO(
            titre=donnees.titre,
            description=donnees.description,
            type_offre=donnees.type_offre,
            type_contrat=donnees.type_contrat,
            type_stage=donnees.type_stage,
            lieu=donnees.lieu,
            date_limite_candidature=donnees.date_limite_candidature,
            salaire_min=donnees.salaire_min,
            salaire_max=donnees.salaire_max,
            competences_requises=donnees.competences_requises,
            experience_requise=donnees.experience_requise,
        )

        # Exécuter le use case
        offre_dto = await use_case.executer(dto, createur_id=utilisateur_courant.id)

        # Convertir le DTO de sortie en schema de réponse
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

    except ValueError as e:
        # Validation EMPLOI/STAGE de l'entité (ou autre ValueError métier)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error": "ValidationError", "message": str(e)},
        )


@router.get(
    "/offres",
    response_model=OffresListResponse,
    summary="Lister mes offres",
    description="Liste toutes les offres créées par l'admin RH connecté",
)
async def lister_mes_offres(
    utilisateur_courant = Depends(get_admin_rh_courant),
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
    utilisateur_courant = Depends(get_admin_rh_courant),
    use_case: PublierOffreUseCase = Depends(get_publier_offre_use_case),
):
    """Publie une offre."""
    try:
        offre_dto = await use_case.executer(offre_id)
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
    except ValueError as e:
        # Transition de statut invalide (ex: offre non en brouillon)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error": "ValidationError", "message": str(e)},
        )


@router.patch(
    "/offres/{offre_id}/cloturer",
    response_model=OffreResponse,
    summary="Clôturer une offre",
    description="Clôture une offre (passe de OUVERTE à CLOTUREE)",
)
async def cloturer_offre(
    offre_id: str,
    utilisateur_courant = Depends(get_admin_rh_courant),
    use_case: CloturerOffreUseCase = Depends(get_cloturer_offre_use_case),
):
    """Clôture une offre."""
    try:
        offre_dto = await use_case.executer(offre_id)
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
    except ValueError as e:
        # Transition de statut invalide (ex: offre non ouverte)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error": "ValidationError", "message": str(e)},
        )