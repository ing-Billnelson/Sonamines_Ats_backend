"""Router pour les opérations sur le profil utilisateur (/moi)."""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from ....application.use_cases import (
    ModifierCanalNotificationUseCase,
    TeleverserPhotoProfilUseCase,
    SupprimerPhotoProfilUseCase,
)
from ....application.dto import ModifierCanalNotificationDTO
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
)
from ..dependencies import (
    get_utilisateur_courant,
    get_modifier_canal_notification_use_case,
    get_televerser_photo_profil_use_case,
    get_supprimer_photo_profil_use_case,
)

router = APIRouter(prefix="/moi", tags=["Profil utilisateur"])
security = HTTPBearer()


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