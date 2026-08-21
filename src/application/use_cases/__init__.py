"""Use cases de la couche application."""

from .ajouter_experience import AjouterExperienceUseCase
from .ajouter_formation import AjouterFormationUseCase
from .ajouter_notes_internes import AjouterNotesInternesUseCase
from .authentifier import AuthentifierUseCase
from .changer_statut_candidature import ChangerStatutCandidatureUseCase
from .cloturer_offre import CloturerOffreUseCase
from .creer_compte_administrateur_rh import CreerCompteAdministrateurRHUseCase
from .creer_compte_candidat import CreerCompteCandidatUseCase
from .creer_offre import CreerOffreUseCase
from .demander_reinitialisation_mot_de_passe import DemanderReinitialisationMotDePasseUseCase
from .lister_candidatures_rh import ListerCandidaturesRHUseCase
from .lister_mes_candidatures import ListerMesCandidaturesUseCase
from .lister_mes_offres import ListerMesOffresUseCase
from .lister_notifications import ListerNotificationsUseCase
from .marquer_notification_lue import MarquerNotificationLueUseCase
from .modifier_canal_notification import ModifierCanalNotificationUseCase
from .modifier_profil_candidat import ModifierProfilCandidatUseCase
from .notifier_utilisateur import NotifierUtilisateurUseCase
from .obtenir_candidature_rh import ObtenirCandidatureRHUseCase
from .obtenir_profil_candidat import ObtenirProfilCandidatUseCase
from .postuler_offre import PostulerOffreUseCase
from .preselectionner_candidat import PreselectionnerCandidatUseCase
from .publier_offre import PublierOffreUseCase
from .rechercher_candidatures import RechercherCandidaturesUseCase
from .rechercher_offres import RechercherOffresUseCase
from .reinitialiser_mot_de_passe import ReinitialiserMotDePasseUseCase
from .soumettre_candidature_spontanee import SoumettreCandidatureSpontaneeUseCase
from .supprimer_experience import SupprimerExperienceUseCase
from .supprimer_formation import SupprimerFormationUseCase
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
    "DemanderReinitialisationMotDePasseUseCase",
    "ReinitialiserMotDePasseUseCase",
    "ModifierCanalNotificationUseCase",
    # Profil candidat
    "ModifierProfilCandidatUseCase",
    "ObtenirProfilCandidatUseCase",
    "AjouterFormationUseCase",
    "SupprimerFormationUseCase",
    "AjouterExperienceUseCase",
    "SupprimerExperienceUseCase",
    # Gestion des fichiers
    "TeleverserPhotoProfilUseCase",
    "SupprimerPhotoProfilUseCase",
    "TeleverserDocumentUseCase",
    # Candidatures
    "SoumettreCandidatureSpontaneeUseCase",
    "PostulerOffreUseCase",
    "ListerMesCandidaturesUseCase",
    "ListerCandidaturesRHUseCase",
    "ChangerStatutCandidatureUseCase",
    "ObtenirCandidatureRHUseCase",
    "AjouterNotesInternesUseCase",
    "PreselectionnerCandidatUseCase",
    # Offres
    "ListerMesOffresUseCase",
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