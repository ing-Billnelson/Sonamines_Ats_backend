"""Schemas Pydantic de l'API v1."""

from .auth_schemas import (
    ConnexionRequest,
    CreerCompteRequest,
    TokenResponse,
    UtilisateurResponse,
    ValiderCompteRequest,
)
from .candidat_schemas import (
    CandidatureResponse,
    DocumentResponse,
    HistoriqueStatutResponse,
    SoumettreKandidatureRequest,
    TeleverserDocumentRequest,
)
from .candidature_schemas import (
    AjouterNotesRequest,
    CandidaturesListResponse,
    ChangerStatutRequest,
    RechercherCandidaturesRequest,
)
from .common_schemas import (
    ErrorResponse,
    FileUploadResponse,
    PaginationResponse,
    SuccessResponse,
)
from .notification_schemas import (
    MarquerLueRequest,
    ModifierCanalNotificationRequest,
    NotificationResponse,
    NotificationsListResponse,
    StatistiquesNotificationsResponse,
)
from .offre_schemas import (
    CreerOffreRequest,
    OffreResponse,
    OffresListResponse,
    RechercherOffresRequest,
)

__all__ = [
    # Auth schemas
    "ConnexionRequest",
    "CreerCompteRequest",
    "TokenResponse",
    "UtilisateurResponse",
    "ValiderCompteRequest",
    # Candidat schemas
    "CandidatureResponse",
    "DocumentResponse",
    "HistoriqueStatutResponse",
    "SoumettreKandidatureRequest",
    "TeleverserDocumentRequest",
    # Candidature schemas (RH)
    "AjouterNotesRequest",
    "CandidaturesListResponse",
    "ChangerStatutRequest",
    "RechercherCandidaturesRequest",
    # Common schemas
    "ErrorResponse",
    "FileUploadResponse",
    "PaginationResponse",
    "SuccessResponse",
    # Notification schemas
    "MarquerLueRequest",
    "ModifierCanalNotificationRequest",
    "NotificationResponse",
    "NotificationsListResponse",
    "StatistiquesNotificationsResponse",
    # Offre schemas
    "CreerOffreRequest",
    "OffreResponse",
    "OffresListResponse",
    "RechercherOffresRequest",
]