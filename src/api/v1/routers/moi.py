"""Router pour les opérations sur le profil utilisateur (/moi)."""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from ....application.use_cases import (
    ModifierCanalNotificationUseCase,
    TeleverserPhotoProfilUseCase,
    SupprimerPhotoProfilUseCase,
    ModifierProfilCandidatUseCase,
    ObtenirProfilCandidatUseCase,
    AjouterFormationUseCase,
    SupprimerFormationUseCase,
    AjouterExperienceUseCase,
    SupprimerExperienceUseCase,
)
from ....application.dto import (
    ModifierCanalNotificationDTO,
    ModifierProfilDTO,
    AjouterFormationDTO,
    AjouterExperienceDTO,
)
from ....application.dto import UtilisateurDTO
from ....domain.exceptions import (
    CanalNonVerifieError,
    UtilisateurIntrouvableError,
    AutorisationRefuseeError,
)
from ..schemas import (
    ModifierCanalNotificationRequest,
    UtilisateurResponse,
    SuccessResponse,
    FileUploadResponse,
    ModifierProfilRequest,
    AjouterFormationRequest,
    AjouterExperienceRequest,
    FormationResponse,
    ExperienceResponse,
)
from ..dependencies import (
    get_utilisateur_courant,
    get_modifier_canal_notification_use_case,
    get_televerser_photo_profil_use_case,
    get_supprimer_photo_profil_use_case,
    get_modifier_profil_candidat_use_case,
    get_obtenir_profil_candidat_use_case,
    get_ajouter_formation_use_case,
    get_supprimer_formation_use_case,
    get_ajouter_experience_use_case,
    get_supprimer_experience_use_case,
)

router = APIRouter(prefix="/moi", tags=["Profil utilisateur"])
security = HTTPBearer()


def _convertir_en_response(utilisateur_dto: UtilisateurDTO) -> UtilisateurResponse:
    """Convertit un UtilisateurDTO en UtilisateurResponse complet."""
    return UtilisateurResponse(
        id=utilisateur_dto.id,
        email=utilisateur_dto.email,
        telephone=utilisateur_dto.telephone,
        nom=utilisateur_dto.nom,
        prenom=utilisateur_dto.prenom,
        nom_complet=utilisateur_dto.nom_complet,
        statut=utilisateur_dto.statut,
        canal_validation=utilisateur_dto.canal_validation,
        email_verifie=utilisateur_dto.email_verifie,
        telephone_verifie=utilisateur_dto.telephone_verifie,
        date_creation=utilisateur_dto.date_creation,
        date_derniere_connexion=utilisateur_dto.date_derniere_connexion,
        photo_url=utilisateur_dto.photo_url,
        role=utilisateur_dto.role,
        linkedin_url=utilisateur_dto.linkedin_url,
        adresse=utilisateur_dto.adresse,
        competences=utilisateur_dto.competences,
        formations=[FormationResponse(**f.__dict__) for f in utilisateur_dto.formations],
        experiences=[ExperienceResponse(**e.__dict__) for e in utilisateur_dto.experiences],
    )


@router.patch(
    "/canal-notification",
    response_model=UtilisateurResponse,
    summary="Modifier le canal de notification",
    description="Modifie le canal de notification de l'utilisateur connecté",
)
async def modifier_canal_notification(
    donnees: ModifierCanalNotificationRequest,
    utilisateur_courant = Depends(get_utilisateur_courant),
    use_case: ModifierCanalNotificationUseCase = Depends(get_modifier_canal_notification_use_case),
):
    """Modifie le canal de notification de l'utilisateur."""
    try:
        # Convertir en DTO
        dto = ModifierCanalNotificationDTO(
            utilisateur_id=utilisateur_courant.id,
            nouveau_canal=donnees.canal,
        )

        # Exécuter le use case
        utilisateur_dto = await use_case.executer(dto)

        return UtilisateurResponse(
            id=utilisateur_dto.id,
            email=utilisateur_dto.email,
            telephone=utilisateur_dto.telephone,
            nom=utilisateur_dto.nom,
            prenom=utilisateur_dto.prenom,
            nom_complet=utilisateur_dto.nom_complet,
            statut=utilisateur_dto.statut,
            canal_validation=utilisateur_dto.canal_validation,
            email_verifie=utilisateur_dto.email_verifie,
            telephone_verifie=utilisateur_dto.telephone_verifie,
            date_creation=utilisateur_dto.date_creation,
            date_derniere_connexion=utilisateur_dto.date_derniere_connexion,
            photo_url=utilisateur_dto.photo_url,
        )

    except CanalNonVerifieError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "CanalNonVerifie", "message": str(e)},
        )
    except UtilisateurIntrouvableError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "UtilisateurIntrouvable", "message": str(e)},
        )


@router.post(
    "/photo",
    response_model=UtilisateurResponse,
    summary="Téléverser une photo de profil",
    description="Téléverse une photo de profil pour le candidat connecté",
)
async def televerser_photo_profil(
    photo: UploadFile = File(..., description="Fichier image (JPG, JPEG, PNG)"),
    utilisateur_courant = Depends(get_utilisateur_courant),
    use_case: TeleverserPhotoProfilUseCase = Depends(get_televerser_photo_profil_use_case),
):
    """Téléverse une photo de profil."""
    try:
        # Lire le contenu du fichier
        contenu_fichier = await photo.read()

        # Exécuter le use case
        utilisateur_dto = await use_case.executer(
            candidat_id=utilisateur_courant.id,
            fichier=contenu_fichier,
            nom_original=photo.filename or "photo_profil",
        )

        return UtilisateurResponse(
            id=utilisateur_dto.id,
            email=utilisateur_dto.email,
            telephone=utilisateur_dto.telephone,
            nom=utilisateur_dto.nom,
            prenom=utilisateur_dto.prenom,
            nom_complet=utilisateur_dto.nom_complet,
            statut=utilisateur_dto.statut,
            canal_validation=utilisateur_dto.canal_validation,
            email_verifie=utilisateur_dto.email_verifie,
            telephone_verifie=utilisateur_dto.telephone_verifie,
            date_creation=utilisateur_dto.date_creation,
            date_derniere_connexion=utilisateur_dto.date_derniere_connexion,
            photo_url=utilisateur_dto.photo_url,
        )

    except AutorisationRefuseeError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": "AutorisationRefusee", "message": str(e)},
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error": "ValidationError", "message": str(e)},
        )


@router.delete(
    "/photo",
    response_model=UtilisateurResponse,
    summary="Supprimer la photo de profil",
    description="Supprime la photo de profil du candidat connecté",
)
async def supprimer_photo_profil(
    utilisateur_courant = Depends(get_utilisateur_courant),
    use_case: SupprimerPhotoProfilUseCase = Depends(get_supprimer_photo_profil_use_case),
):
    """Supprime la photo de profil."""
    try:
        # Exécuter le use case
        utilisateur_dto = await use_case.executer(candidat_id=utilisateur_courant.id)

        return UtilisateurResponse(
            id=utilisateur_dto.id,
            email=utilisateur_dto.email,
            telephone=utilisateur_dto.telephone,
            nom=utilisateur_dto.nom,
            prenom=utilisateur_dto.prenom,
            nom_complet=utilisateur_dto.nom_complet,
            statut=utilisateur_dto.statut,
            canal_validation=utilisateur_dto.canal_validation,
            email_verifie=utilisateur_dto.email_verifie,
            telephone_verifie=utilisateur_dto.telephone_verifie,
            date_creation=utilisateur_dto.date_creation,
            date_derniere_connexion=utilisateur_dto.date_derniere_connexion,
            photo_url=utilisateur_dto.photo_url,
        )

    except AutorisationRefuseeError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": "AutorisationRefusee", "message": str(e)},
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "ValidationError", "message": str(e)},
        )


@router.get(
    "/profil",
    response_model=UtilisateurResponse,
    summary="Obtenir le profil candidat complet",
    description="Retourne le profil du candidat connecté avec ses formations et expériences",
)
async def obtenir_profil_candidat(
    utilisateur_courant = Depends(get_utilisateur_courant),
    use_case: ObtenirProfilCandidatUseCase = Depends(get_obtenir_profil_candidat_use_case),
):
    """Récupère le profil complet du candidat connecté."""
    try:
        utilisateur_dto = await use_case.executer(candidat_id=utilisateur_courant.id)
        return _convertir_en_response(utilisateur_dto)
    except UtilisateurIntrouvableError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "UtilisateurIntrouvable", "message": str(e)},
        )


@router.patch(
    "/profil",
    response_model=UtilisateurResponse,
    summary="Modifier le profil candidat",
    description="Modifie nom/prénom/téléphone/linkedin/adresse/compétences du candidat connecté",
)
async def modifier_profil_candidat(
    donnees: ModifierProfilRequest,
    utilisateur_courant = Depends(get_utilisateur_courant),
    use_case: ModifierProfilCandidatUseCase = Depends(get_modifier_profil_candidat_use_case),
):
    """Modifie le profil du candidat connecté."""
    try:
        dto = ModifierProfilDTO(
            candidat_id=utilisateur_courant.id,
            nom=donnees.nom,
            prenom=donnees.prenom,
            telephone=donnees.telephone,
            linkedin_url=donnees.linkedin_url,
            adresse=donnees.adresse,
            competences=donnees.competences,
        )
        utilisateur_dto = await use_case.executer(dto)
        return _convertir_en_response(utilisateur_dto)
    except UtilisateurIntrouvableError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "UtilisateurIntrouvable", "message": str(e)},
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error": "ValidationError", "message": str(e)},
        )


@router.post(
    "/formations",
    response_model=FormationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Ajouter une formation",
    description="Ajoute une formation au profil du candidat connecté",
)
async def ajouter_formation(
    donnees: AjouterFormationRequest,
    utilisateur_courant = Depends(get_utilisateur_courant),
    use_case: AjouterFormationUseCase = Depends(get_ajouter_formation_use_case),
):
    """Ajoute une formation au candidat connecté."""
    try:
        dto = AjouterFormationDTO(
            candidat_id=utilisateur_courant.id,
            etablissement=donnees.etablissement,
            diplome=donnees.diplome,
            annee_debut=donnees.annee_debut,
            annee_fin=donnees.annee_fin,
        )
        formation_dto = await use_case.executer(dto)
        return FormationResponse(
            id=formation_dto.id,
            etablissement=formation_dto.etablissement,
            diplome=formation_dto.diplome,
            annee_debut=formation_dto.annee_debut,
            annee_fin=formation_dto.annee_fin,
        )
    except UtilisateurIntrouvableError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "UtilisateurIntrouvable", "message": str(e)},
        )


@router.delete(
    "/formations/{formation_id}",
    response_model=SuccessResponse,
    summary="Supprimer une formation",
    description="Supprime une formation du profil du candidat connecté",
)
async def supprimer_formation(
    formation_id: str,
    utilisateur_courant = Depends(get_utilisateur_courant),
    use_case: SupprimerFormationUseCase = Depends(get_supprimer_formation_use_case),
):
    """Supprime une formation du candidat connecté."""
    try:
        supprime = await use_case.executer(
            candidat_id=utilisateur_courant.id,
            formation_id=formation_id,
        )
        if not supprime:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "FormationIntrouvable", "message": "Formation introuvable"},
            )
        return SuccessResponse(success=True, message="Formation supprimée avec succès")
    except UtilisateurIntrouvableError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "UtilisateurIntrouvable", "message": str(e)},
        )


@router.post(
    "/experiences",
    response_model=ExperienceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Ajouter une expérience",
    description="Ajoute une expérience professionnelle au profil du candidat connecté",
)
async def ajouter_experience(
    donnees: AjouterExperienceRequest,
    utilisateur_courant = Depends(get_utilisateur_courant),
    use_case: AjouterExperienceUseCase = Depends(get_ajouter_experience_use_case),
):
    """Ajoute une expérience au candidat connecté."""
    try:
        dto = AjouterExperienceDTO(
            candidat_id=utilisateur_courant.id,
            entreprise=donnees.entreprise,
            poste=donnees.poste,
            date_debut=donnees.date_debut,
            date_fin=donnees.date_fin,
            description=donnees.description,
        )
        experience_dto = await use_case.executer(dto)
        return ExperienceResponse(
            id=experience_dto.id,
            entreprise=experience_dto.entreprise,
            poste=experience_dto.poste,
            date_debut=experience_dto.date_debut,
            date_fin=experience_dto.date_fin,
            description=experience_dto.description,
        )
    except UtilisateurIntrouvableError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "UtilisateurIntrouvable", "message": str(e)},
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error": "ValidationError", "message": str(e)},
        )


@router.delete(
    "/experiences/{experience_id}",
    response_model=SuccessResponse,
    summary="Supprimer une expérience",
    description="Supprime une expérience du profil du candidat connecté",
)
async def supprimer_experience(
    experience_id: str,
    utilisateur_courant = Depends(get_utilisateur_courant),
    use_case: SupprimerExperienceUseCase = Depends(get_supprimer_experience_use_case),
):
    """Supprime une expérience du candidat connecté."""
    try:
        supprime = await use_case.executer(
            candidat_id=utilisateur_courant.id,
            experience_id=experience_id,
        )
        if not supprime:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "ExperienceIntrouvable", "message": "Expérience introuvable"},
            )
        return SuccessResponse(success=True, message="Expérience supprimée avec succès")
    except UtilisateurIntrouvableError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "UtilisateurIntrouvable", "message": str(e)},
        )