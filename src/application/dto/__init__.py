"""DTOs de la couche application."""

from .candidature_dto import (
    AjouterNotesInternesDTO,
    CandidatureDTO,
    ChangerStatutCandidatureDTO,
    DocumentDTO,
    HistoriqueStatutDTO,
    RechercherCandidaturesDTO,
    SoumettreKandidatureDTO,
    TeleverserDocumentDTO,
)
from .compte_dto import (
    AuthentificationDTO,
    CreerCompteDTO,
    DemanderReinitialisationDTO,
    ModifierCanalNotificationDTO,
    ReinitialiserMotDePasseDTO,
    TokenDTO,
    UtilisateurDTO,
    ValiderCompteDTO,
    ModifierProfilDTO,
    FormationDTO,
    AjouterFormationDTO,
    ExperienceDTO,
    AjouterExperienceDTO,
)
from .notification_dto import (
    ListerNotificationsDTO,
    MarquerNotificationLueDTO,
    NotificationDTO,
    StatistiquesNotificationsDTO,
)
from .offre_dto import (
    CreerOffreDTO,
    ModifierOffreDTO,
    OffreDTO,
    RechercherOffresDTO,
)
from .recherche_dto import (
    FacetteRechercheDTO,
    ResultatRechercheAvanceeDTO,
    ResultatRechercheDTO,
)

__all__ = [
    # Compte DTOs
    "AuthentificationDTO",
    "CreerCompteDTO",
    "DemanderReinitialisationDTO",
    "ModifierCanalNotificationDTO",
    "ReinitialiserMotDePasseDTO",
    "TokenDTO",
    "UtilisateurDTO",
    "ValiderCompteDTO",
    "ModifierProfilDTO",
    "FormationDTO",
    "AjouterFormationDTO",
    "ExperienceDTO",
    "AjouterExperienceDTO",
    # Offre DTOs
    "CreerOffreDTO",
    "ModifierOffreDTO",
    "OffreDTO",
    "RechercherOffresDTO",
    # Candidature DTOs
    "AjouterNotesInternesDTO",
    "CandidatureDTO",
    "ChangerStatutCandidatureDTO",
    "DocumentDTO",
    "HistoriqueStatutDTO",
    "RechercherCandidaturesDTO",
    "SoumettreKandidatureDTO",
    "TeleverserDocumentDTO",
    # Notification DTOs
    "ListerNotificationsDTO",
    "MarquerNotificationLueDTO",
    "NotificationDTO",
    "StatistiquesNotificationsDTO",
    # Recherche DTOs
    "FacetteRechercheDTO",
    "ResultatRechercheAvanceeDTO",
    "ResultatRechercheDTO",
]