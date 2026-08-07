"""Dépendances FastAPI pour l'injection de dépendances."""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from argon2 import PasswordHasher

from ...application.use_cases import (
    CreerCompteCandidatUseCase,
    AuthentifierUseCase,
    ModifierCanalNotificationUseCase,
    TeleverserPhotoProfilUseCase,
    SupprimerPhotoProfilUseCase,
    SoumettreCandidatureSpontaneeUseCase,
    TeleverserDocumentUseCase,
    ListerNotificationsUseCase,
    MarquerNotificationLueUseCase,
    NotifierUtilisateurUseCase,
)
from ...application.dto import UtilisateurDTO
from ...domain.exceptions import AuthentificationEchoueeError
from ...infrastructure.config import settings

# Configuration de la sécurité
security = HTTPBearer()


# Singletons et factories
def get_password_hasher() -> PasswordHasher:
    """Retourne une instance du hasher de mots de passe."""
    return PasswordHasher()


def get_settings():
    """Retourne la configuration de l'application."""
    return settings


# Use cases factories (stubs pour l'instant)
def get_creer_compte_candidat_use_case() -> CreerCompteCandidatUseCase:
    """Factory pour le use case de création de compte candidat."""
    # TODO: Implémenter l'injection des vraies dépendances
    password_hasher = get_password_hasher()
    # Ces imports seront à faire quand les repositories seront implémentés
    # return CreerCompteCandidatUseCase(
    #     utilisateur_repository=get_utilisateur_repository(),
    #     notifier_utilisateur=get_notifier_utilisateur_use_case(),
    #     password_hasher=password_hasher,
    # )
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail={"error": "NotImplemented", "message": "Use case non configuré"},
    )


def get_authentifier_use_case() -> AuthentifierUseCase:
    """Factory pour le use case d'authentification."""
    # TODO: Implémenter l'injection des vraies dépendances
    password_hasher = get_password_hasher()
    # return AuthentifierUseCase(
    #     utilisateur_repository=get_utilisateur_repository(),
    #     password_hasher=password_hasher,
    #     jwt_secret_key=settings.jwt_secret_key,
    #     jwt_algorithm=settings.jwt_algorithm,
    #     jwt_expire_minutes=settings.jwt_access_token_expire_minutes,
    # )
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail={"error": "NotImplemented", "message": "Use case non configuré"},
    )


def get_modifier_canal_notification_use_case() -> ModifierCanalNotificationUseCase:
    """Factory pour le use case de modification de canal."""
    # TODO: Implémenter l'injection des vraies dépendances
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail={"error": "NotImplemented", "message": "Use case non configuré"},
    )


def get_televerser_photo_profil_use_case() -> TeleverserPhotoProfilUseCase:
    """Factory pour le use case de téléversement de photo."""
    # TODO: Implémenter l'injection des vraies dépendances
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail={"error": "NotImplemented", "message": "Use case non configuré"},
    )


def get_soumettre_candidature_spontanee_use_case() -> SoumettreCandidatureSpontaneeUseCase:
    """Factory pour le use case de candidature spontanée."""
    # TODO: Implémenter l'injection des vraies dépendances
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail={"error": "NotImplemented", "message": "Use case non configuré"},
    )


def get_televerser_document_use_case() -> TeleverserDocumentUseCase:
    """Factory pour le use case de téléversement de document."""
    # TODO: Implémenter l'injection des vraies dépendances
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail={"error": "NotImplemented", "message": "Use case non configuré"},
    )


def get_lister_notifications_use_case() -> ListerNotificationsUseCase:
    """Factory pour le use case de listage de notifications."""
    # TODO: Implémenter l'injection des vraies dépendances
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail={"error": "NotImplemented", "message": "Use case non configuré"},
    )


def get_marquer_notification_lue_use_case() -> MarquerNotificationLueUseCase:
    """Factory pour le use case de marquage de notification."""
    # TODO: Implémenter l'injection des vraies dépendances
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail={"error": "NotImplemented", "message": "Use case non configuré"},
    )


# Authentification et autorisation
async def get_utilisateur_courant(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_use_case: AuthentifierUseCase = Depends(get_authentifier_use_case),
) -> UtilisateurDTO:
    """Récupère l'utilisateur connecté à partir du token JWT."""
    try:
        utilisateur_dto = await auth_use_case.verifier_token(credentials.credentials)
        return utilisateur_dto
    except AuthentificationEchoueeError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "TokenInvalide", "message": str(e)},
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_admin_rh_courant(
    utilisateur_courant: UtilisateurDTO = Depends(get_utilisateur_courant),
) -> UtilisateurDTO:
    """Vérifie que l'utilisateur connecté est un Admin RH."""
    # TODO: Implémenter la vérification du rôle
    # Pour l'instant, on accepte tous les utilisateurs connectés
    return utilisateur_courant


def get_super_admin_courant(
    utilisateur_courant: UtilisateurDTO = Depends(get_utilisateur_courant),
) -> UtilisateurDTO:
    """Vérifie que l'utilisateur connecté est un Super Admin."""
    # TODO: Implémenter la vérification du rôle
    # Pour l'instant, on accepte tous les utilisateurs connectés
    return utilisateur_courant