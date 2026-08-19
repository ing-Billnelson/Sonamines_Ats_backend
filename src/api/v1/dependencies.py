"""Dépendances FastAPI pour l'injection de dépendances."""

from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from argon2 import PasswordHasher
from sqlalchemy.ext.asyncio import AsyncSession

from ...application.use_cases import (
    CreerCompteCandidatUseCase,
    CreerCompteAdministrateurRHUseCase,
    AuthentifierUseCase,
    ModifierCanalNotificationUseCase,
    TeleverserPhotoProfilUseCase,
    SupprimerPhotoProfilUseCase,
    SoumettreCandidatureSpontaneeUseCase,
    PostulerOffreUseCase,
    TeleverserDocumentUseCase,
    ListerNotificationsUseCase,
    MarquerNotificationLueUseCase,
    NotifierUtilisateurUseCase,
    ValiderCompteUseCase,
    DemanderReinitialisationMotDePasseUseCase,
    ReinitialiserMotDePasseUseCase,
    ModifierProfilCandidatUseCase,
    ObtenirProfilCandidatUseCase,
    AjouterFormationUseCase,
    SupprimerFormationUseCase,
    AjouterExperienceUseCase,
    SupprimerExperienceUseCase,
    ListerMesOffresUseCase,
    CreerOffreUseCase,
    PublierOffreUseCase,
    CloturerOffreUseCase,
    RechercherOffresUseCase,
)
from ...application.dto import UtilisateurDTO
from ...domain.entities import AdministrateurRH, SuperAdministrateur
from ...domain.exceptions import AuthentificationEchoueeError
from ...domain.ports import NotificationRepository, ProfilCandidatRepository
from ...infrastructure.config import settings
from ...infrastructure.db.session import get_db
from ...infrastructure.db.repositories import (
    PostgresUtilisateurRepository,
    PostgresCandidatureRepository,
    PostgresOffreRepository,
    PostgresNotificationRepository,
    PostgresProfilCandidatRepository,
)
from ...infrastructure.notification import EmailAdapter, SMSAdapter, NotificationRouter
from ...infrastructure.search import ElasticsearchAdapter
from ...infrastructure.storage import MinioAdapter

# Configuration de la sécurité
security = HTTPBearer()


# === Repositories & Adapters d'infrastructure ===

def get_utilisateur_repository(
    session: AsyncSession = Depends(get_db)
) -> PostgresUtilisateurRepository:
    """Factory pour le repository utilisateur PostgreSQL."""
    return PostgresUtilisateurRepository(session)


def get_candidature_repository(
    session: AsyncSession = Depends(get_db)
) -> PostgresCandidatureRepository:
    """Factory pour le repository candidature PostgreSQL."""
    return PostgresCandidatureRepository(session)


def get_offre_repository(
    session: AsyncSession = Depends(get_db)
) -> PostgresOffreRepository:
    """Factory pour le repository offre PostgreSQL."""
    return PostgresOffreRepository(session)


def get_notification_repository(
    session: AsyncSession = Depends(get_db)
) -> PostgresNotificationRepository:
    """Factory pour le repository notification PostgreSQL."""
    return PostgresNotificationRepository(session)


def get_profil_candidat_repository(
    session: AsyncSession = Depends(get_db)
) -> PostgresProfilCandidatRepository:
    """Factory pour le repository profil candidat PostgreSQL."""
    return PostgresProfilCandidatRepository(session)


def get_email_adapter() -> EmailAdapter:
    """Factory pour l'adapter email."""
    return EmailAdapter(settings)


def get_sms_adapter() -> SMSAdapter:
    """Factory pour l'adapter SMS."""
    return SMSAdapter(settings)


def get_notification_router(
    email_adapter: EmailAdapter = Depends(get_email_adapter),
    sms_adapter: SMSAdapter = Depends(get_sms_adapter),
) -> NotificationRouter:
    """Factory pour le routeur de notifications composite."""
    return NotificationRouter(email_adapter=email_adapter, sms_adapter=sms_adapter)


def get_search_adapter() -> ElasticsearchAdapter:
    """Factory pour l'adapter Elasticsearch."""
    return ElasticsearchAdapter(settings)


def get_storage_adapter() -> MinioAdapter:
    """Factory pour l'adapter MinIO."""
    return MinioAdapter(settings)


# === Utilitaires ===
def get_password_hasher() -> PasswordHasher:
    """Retourne une instance du hasher de mots de passe."""
    return PasswordHasher()


def get_settings():
    """Retourne la configuration de l'application."""
    return settings


# === Use cases factories ===

def get_notifier_utilisateur_use_case(
    notification_repository: NotificationRepository = Depends(get_notification_repository),
    notification_port: NotificationRouter = Depends(get_notification_router),
) -> NotifierUtilisateurUseCase:
    """Factory pour le use case de notification des utilisateurs."""
    return NotifierUtilisateurUseCase(
        notification_repository=notification_repository,
        notification_port=notification_port,
    )


def get_creer_compte_candidat_use_case(
    utilisateur_repository: PostgresUtilisateurRepository = Depends(get_utilisateur_repository),
    notifier_utilisateur: NotifierUtilisateurUseCase = Depends(get_notifier_utilisateur_use_case),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
) -> CreerCompteCandidatUseCase:
    """Factory pour le use case de création de compte candidat."""
    return CreerCompteCandidatUseCase(
        utilisateur_repository=utilisateur_repository,
        notifier_utilisateur=notifier_utilisateur,
        password_hasher=password_hasher,
    )


def get_creer_compte_administrateur_rh_use_case(
    utilisateur_repository: PostgresUtilisateurRepository = Depends(get_utilisateur_repository),
    notifier_utilisateur: NotifierUtilisateurUseCase = Depends(get_notifier_utilisateur_use_case),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
) -> CreerCompteAdministrateurRHUseCase:
    """Factory pour le use case de création de compte administrateur RH."""
    return CreerCompteAdministrateurRHUseCase(
        utilisateur_repository=utilisateur_repository,
        notifier_utilisateur=notifier_utilisateur,
        password_hasher=password_hasher,
    )


def get_authentifier_use_case(
    utilisateur_repository: PostgresUtilisateurRepository = Depends(get_utilisateur_repository),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
    app_settings = Depends(get_settings),
) -> AuthentifierUseCase:
    """Factory pour le use case d'authentification."""
    return AuthentifierUseCase(
        utilisateur_repository=utilisateur_repository,
        password_hasher=password_hasher,
        jwt_secret_key=app_settings.jwt_secret_key,
        jwt_algorithm=app_settings.jwt_algorithm,
        jwt_expire_minutes=app_settings.jwt_access_token_expire_minutes,
    )


def get_valider_compte_use_case(
    utilisateur_repository: PostgresUtilisateurRepository = Depends(get_utilisateur_repository),
    notifier_utilisateur: NotifierUtilisateurUseCase = Depends(get_notifier_utilisateur_use_case),
) -> ValiderCompteUseCase:
    """Factory pour le use case de validation de compte."""
    return ValiderCompteUseCase(
        utilisateur_repository=utilisateur_repository,
        notifier_utilisateur=notifier_utilisateur,
    )


def get_demander_reinitialisation_mot_de_passe_use_case(
    utilisateur_repository: PostgresUtilisateurRepository = Depends(get_utilisateur_repository),
    notifier_utilisateur: NotifierUtilisateurUseCase = Depends(get_notifier_utilisateur_use_case),
) -> DemanderReinitialisationMotDePasseUseCase:
    """Factory pour le use case de demande de réinitialisation de mot de passe."""
    return DemanderReinitialisationMotDePasseUseCase(
        utilisateur_repository=utilisateur_repository,
        notifier_utilisateur=notifier_utilisateur,
    )


def get_reinitialiser_mot_de_passe_use_case(
    utilisateur_repository: PostgresUtilisateurRepository = Depends(get_utilisateur_repository),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
) -> ReinitialiserMotDePasseUseCase:
    """Factory pour le use case de réinitialisation de mot de passe."""
    return ReinitialiserMotDePasseUseCase(
        utilisateur_repository=utilisateur_repository,
        password_hasher=password_hasher,
    )


def get_modifier_canal_notification_use_case() -> ModifierCanalNotificationUseCase:
    """Factory pour le use case de modification de canal."""
    # TODO: Implémenter l'injection des vraies dépendances
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail={"error": "NotImplemented", "message": "Use case non configuré"},
    )


def get_televerser_photo_profil_use_case(
    utilisateur_repository: PostgresUtilisateurRepository = Depends(get_utilisateur_repository),
    storage_port: MinioAdapter = Depends(get_storage_adapter),
) -> TeleverserPhotoProfilUseCase:
    """Factory pour le use case de téléversement de photo."""
    return TeleverserPhotoProfilUseCase(
        utilisateur_repository=utilisateur_repository,
        storage_port=storage_port,
    )


def get_supprimer_photo_profil_use_case(
    utilisateur_repository: PostgresUtilisateurRepository = Depends(get_utilisateur_repository),
    storage_port: MinioAdapter = Depends(get_storage_adapter),
) -> SupprimerPhotoProfilUseCase:
    """Factory pour le use case de suppression de photo."""
    return SupprimerPhotoProfilUseCase(
        utilisateur_repository=utilisateur_repository,
        storage_port=storage_port,
    )


def get_modifier_profil_candidat_use_case(
    utilisateur_repository: PostgresUtilisateurRepository = Depends(get_utilisateur_repository),
    profil_candidat_repository: ProfilCandidatRepository = Depends(get_profil_candidat_repository),
) -> ModifierProfilCandidatUseCase:
    """Factory pour le use case de modification du profil candidat."""
    return ModifierProfilCandidatUseCase(
        utilisateur_repository=utilisateur_repository,
        profil_candidat_repository=profil_candidat_repository,
    )


def get_obtenir_profil_candidat_use_case(
    utilisateur_repository: PostgresUtilisateurRepository = Depends(get_utilisateur_repository),
    profil_candidat_repository: ProfilCandidatRepository = Depends(get_profil_candidat_repository),
) -> ObtenirProfilCandidatUseCase:
    """Factory pour le use case de récupération du profil candidat."""
    return ObtenirProfilCandidatUseCase(
        utilisateur_repository=utilisateur_repository,
        profil_candidat_repository=profil_candidat_repository,
    )


def get_ajouter_formation_use_case(
    utilisateur_repository: PostgresUtilisateurRepository = Depends(get_utilisateur_repository),
    profil_candidat_repository: ProfilCandidatRepository = Depends(get_profil_candidat_repository),
) -> AjouterFormationUseCase:
    """Factory pour le use case d'ajout de formation."""
    return AjouterFormationUseCase(
        utilisateur_repository=utilisateur_repository,
        profil_candidat_repository=profil_candidat_repository,
    )


def get_supprimer_formation_use_case(
    utilisateur_repository: PostgresUtilisateurRepository = Depends(get_utilisateur_repository),
    profil_candidat_repository: ProfilCandidatRepository = Depends(get_profil_candidat_repository),
) -> SupprimerFormationUseCase:
    """Factory pour le use case de suppression de formation."""
    return SupprimerFormationUseCase(
        utilisateur_repository=utilisateur_repository,
        profil_candidat_repository=profil_candidat_repository,
    )


def get_ajouter_experience_use_case(
    utilisateur_repository: PostgresUtilisateurRepository = Depends(get_utilisateur_repository),
    profil_candidat_repository: ProfilCandidatRepository = Depends(get_profil_candidat_repository),
) -> AjouterExperienceUseCase:
    """Factory pour le use case d'ajout d'expérience."""
    return AjouterExperienceUseCase(
        utilisateur_repository=utilisateur_repository,
        profil_candidat_repository=profil_candidat_repository,
    )


def get_supprimer_experience_use_case(
    utilisateur_repository: PostgresUtilisateurRepository = Depends(get_utilisateur_repository),
    profil_candidat_repository: ProfilCandidatRepository = Depends(get_profil_candidat_repository),
) -> SupprimerExperienceUseCase:
    """Factory pour le use case de suppression d'expérience."""
    return SupprimerExperienceUseCase(
        utilisateur_repository=utilisateur_repository,
        profil_candidat_repository=profil_candidat_repository,
    )


def get_soumettre_candidature_spontanee_use_case(
    candidature_repository: PostgresCandidatureRepository = Depends(get_candidature_repository),
    utilisateur_repository: PostgresUtilisateurRepository = Depends(get_utilisateur_repository),
    notifier_utilisateur: NotifierUtilisateurUseCase = Depends(get_notifier_utilisateur_use_case),
) -> SoumettreCandidatureSpontaneeUseCase:
    """Factory pour le use case de candidature spontanée."""
    return SoumettreCandidatureSpontaneeUseCase(
        candidature_repository=candidature_repository,
        utilisateur_repository=utilisateur_repository,
        notifier_utilisateur=notifier_utilisateur,
    )


def get_postuler_offre_use_case(
    candidature_repository: PostgresCandidatureRepository = Depends(get_candidature_repository),
    offre_repository: PostgresOffreRepository = Depends(get_offre_repository),
    utilisateur_repository: PostgresUtilisateurRepository = Depends(get_utilisateur_repository),
    notifier_utilisateur: NotifierUtilisateurUseCase = Depends(get_notifier_utilisateur_use_case),
) -> PostulerOffreUseCase:
    """Factory pour le use case de candidature à une offre."""
    return PostulerOffreUseCase(
        candidature_repository=candidature_repository,
        offre_repository=offre_repository,
        utilisateur_repository=utilisateur_repository,
        notifier_utilisateur=notifier_utilisateur,
    )


def get_creer_offre_use_case(
    offre_repository: PostgresOffreRepository = Depends(get_offre_repository),
    utilisateur_repository: PostgresUtilisateurRepository = Depends(get_utilisateur_repository),
    search_port: ElasticsearchAdapter = Depends(get_search_adapter),
) -> CreerOffreUseCase:
    """Factory pour le use case de création d'offre."""
    return CreerOffreUseCase(
        offre_repository=offre_repository,
        utilisateur_repository=utilisateur_repository,
        search_port=search_port,
    )


def get_publier_offre_use_case(
    offre_repository: PostgresOffreRepository = Depends(get_offre_repository),
    utilisateur_repository: PostgresUtilisateurRepository = Depends(get_utilisateur_repository),
    search_port: ElasticsearchAdapter = Depends(get_search_adapter),
) -> PublierOffreUseCase:
    """Factory pour le use case de publication d'offre."""
    return PublierOffreUseCase(
        offre_repository=offre_repository,
        utilisateur_repository=utilisateur_repository,
        search_port=search_port,
    )


def get_cloturer_offre_use_case(
    offre_repository: PostgresOffreRepository = Depends(get_offre_repository),
    utilisateur_repository: PostgresUtilisateurRepository = Depends(get_utilisateur_repository),
    search_port: ElasticsearchAdapter = Depends(get_search_adapter),
) -> CloturerOffreUseCase:
    """Factory pour le use case de clôture d'offre."""
    return CloturerOffreUseCase(
        offre_repository=offre_repository,
        utilisateur_repository=utilisateur_repository,
        search_port=search_port,
    )


def get_lister_mes_offres_use_case(
    offre_repository: PostgresOffreRepository = Depends(get_offre_repository),
    utilisateur_repository: PostgresUtilisateurRepository = Depends(get_utilisateur_repository),
) -> ListerMesOffresUseCase:
    """Factory pour le use case de listage des offres d'un admin RH."""
    return ListerMesOffresUseCase(
        offre_repository=offre_repository,
        utilisateur_repository=utilisateur_repository,
    )


def get_rechercher_offres_use_case(
    search_port: ElasticsearchAdapter = Depends(get_search_adapter),
    offre_repository: PostgresOffreRepository = Depends(get_offre_repository),
) -> RechercherOffresUseCase:
    """Factory pour le use case de recherche d'offres."""
    return RechercherOffresUseCase(
        search_port=search_port,
        offre_repository=offre_repository,
    )


def get_televerser_document_use_case(
    candidature_repository: PostgresCandidatureRepository = Depends(get_candidature_repository),
    storage_port: MinioAdapter = Depends(get_storage_adapter),
) -> TeleverserDocumentUseCase:
    """Factory pour le use case de téléversement de document."""
    return TeleverserDocumentUseCase(
        candidature_repository=candidature_repository,
        storage_port=storage_port,
    )


def get_lister_notifications_use_case(
    notification_repository: PostgresNotificationRepository = Depends(get_notification_repository),
) -> ListerNotificationsUseCase:
    """Factory pour le use case de listage de notifications."""
    return ListerNotificationsUseCase(
        notification_repository=notification_repository,
    )


def get_marquer_notification_lue_use_case(
    notification_repository: PostgresNotificationRepository = Depends(get_notification_repository),
) -> MarquerNotificationLueUseCase:
    """Factory pour le use case de marquage de notification."""
    return MarquerNotificationLueUseCase(
        notification_repository=notification_repository,
    )


# === Authentification et autorisation ===
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


async def get_admin_rh_courant(
    utilisateur_courant: UtilisateurDTO = Depends(get_utilisateur_courant),
    utilisateur_repository: PostgresUtilisateurRepository = Depends(get_utilisateur_repository),
) -> UtilisateurDTO:
    """Vérifie que l'utilisateur connecté est un Admin RH (ou Super Admin)."""
    utilisateur = await utilisateur_repository.obtenir_par_id(UUID(utilisateur_courant.id))
    if utilisateur is None or not isinstance(
        utilisateur, (AdministrateurRH, SuperAdministrateur)
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": "AccesRefuse", "message": "Accès réservé aux administrateurs RH"},
        )
    return utilisateur_courant


async def get_super_admin_courant(
    utilisateur_courant: UtilisateurDTO = Depends(get_utilisateur_courant),
    utilisateur_repository: PostgresUtilisateurRepository = Depends(get_utilisateur_repository),
) -> UtilisateurDTO:
    """Vérifie que l'utilisateur connecté est un Super Admin."""
    utilisateur = await utilisateur_repository.obtenir_par_id(UUID(utilisateur_courant.id))
    if utilisateur is None or not isinstance(utilisateur, SuperAdministrateur):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": "AccesRefuse", "message": "Accès réservé aux super administrateurs"},
        )
    return utilisateur_courant