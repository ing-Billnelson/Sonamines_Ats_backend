"""Use cases de la couche application."""

from .authentifier import AuthentifierUseCase
from .changer_statut_candidature import ChangerStatutCandidatureUseCase
from .cloturer_offre import CloturerOffreUseCase
from .creer_compte_administrateur_rh import CreerCompteAdministrateurRHUseCase
from .creer_compte_candidat import CreerCompteCandidatUseCase
from .creer_offre import CreerOffreUseCase
from .lister_notifications import ListerNotificationsUseCase
from .marquer_notification_lue import MarquerNotificationLueUseCase
from .modifier_canal_notification import ModifierCanalNotificationUseCase
from .notifier_utilisateur import NotifierUtilisateurUseCase
from .postuler_offre import PostulerOffreUseCase
from .preselectionner_candidat import PreselectionnerCandidatUseCase
from .publier_offre import PublierOffreUseCase
from .rechercher_candidatures import RechercherCandidaturesUseCase
from .rechercher_offres import RechercherOffresUseCase
from .soumettre_candidature_spontanee import SoumettreCandidatureSpontaneeUseCase
from .supprimer_photo_profil import SupprimerPhotoProfilUseCase
from .televerser_document import TeleverserDocumentUseCase
from .televerser_photo_profil import TeleverserPhotoProfilUseCase
from .valider_compte import ValiderCompteUseCase

__all__ = [
    # Authentification et comptes
    "AuthentifierUseCase",
    "CreerCompteCandidatUseCase",
    "CreerCompteAdministrateurRHUseCase",
    "ValiderCompteUseCase",
    "ModifierCanalNotificationUseCase",
    # Gestion des fichiers
    "TeleverserPhotoProfilUseCase",
    "SupprimerPhotoProfilUseCase",
    "TeleverserDocumentUseCase",
    # Candidatures
    "SoumettreCandidatureSpontaneeUseCase",
    "PostulerOffreUseCase",
    "ChangerStatutCandidatureUseCase",
    "PreselectionnerCandidatUseCase",
    # Offres
    "CreerOffreUseCase",
    "PublierOffreUseCase",
    "CloturerOffreUseCase",
    # Recherche
    "RechercherCandidaturesUseCase",
    "RechercherOffresUseCase",
    # Notifications
    "NotifierUtilisateurUseCase",
    "ListerNotificationsUseCase",
    "MarquerNotificationLueUseCase",
]