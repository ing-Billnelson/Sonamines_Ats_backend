"""Modèles SQLAlchemy de l'infrastructure."""

from .candidature_model import CandidatureModel
from .document_model import DocumentModel
from .experience_model import ExperienceModel
from .formation_model import FormationModel
from .historique_statut_model import HistoriqueStatutModel
from .notification_model import NotificationModel
from .offre_model import OffreModel
from .utilisateur_model import (
    Base,
    UtilisateurModel,
    CandidatModel,
    AdministrateurModel,
    AdministrateurRHModel,
    SuperAdministrateurModel,
)

# Ajouter les relations après import de tous les modèles
from sqlalchemy.orm import relationship

# Relations pour UtilisateurModel
UtilisateurModel.offres_creees = relationship("OffreModel", foreign_keys="OffreModel.createur_id")
UtilisateurModel.candidatures = relationship("CandidatureModel", foreign_keys="CandidatureModel.candidat_id")
UtilisateurModel.notifications = relationship("NotificationModel", foreign_keys="NotificationModel.utilisateur_id")
UtilisateurModel.formations = relationship("FormationModel", foreign_keys="FormationModel.candidat_id", cascade="all, delete-orphan")
UtilisateurModel.experiences = relationship("ExperienceModel", foreign_keys="ExperienceModel.candidat_id", cascade="all, delete-orphan")

# Relations pour OffreModel  
OffreModel.createur = relationship("UtilisateurModel", foreign_keys="OffreModel.createur_id")
OffreModel.candidatures = relationship("CandidatureModel", foreign_keys="CandidatureModel.offre_id")

# Relations pour CandidatureModel
CandidatureModel.candidat = relationship("UtilisateurModel", foreign_keys="CandidatureModel.candidat_id")
CandidatureModel.offre = relationship("OffreModel", foreign_keys="CandidatureModel.offre_id")
CandidatureModel.documents = relationship("DocumentModel", foreign_keys="DocumentModel.candidature_id", cascade="all, delete-orphan")
CandidatureModel.historique_statuts = relationship("HistoriqueStatutModel", foreign_keys="HistoriqueStatutModel.candidature_id", cascade="all, delete-orphan")

# Relations pour DocumentModel
DocumentModel.candidature = relationship("CandidatureModel", foreign_keys="DocumentModel.candidature_id")
DocumentModel.telechargeur = relationship("UtilisateurModel", foreign_keys="DocumentModel.telechargeur_id")

# Relations pour NotificationModel
NotificationModel.utilisateur = relationship("UtilisateurModel", foreign_keys="NotificationModel.utilisateur_id")

# Relations pour HistoriqueStatutModel
HistoriqueStatutModel.candidature = relationship("CandidatureModel", foreign_keys="HistoriqueStatutModel.candidature_id")
HistoriqueStatutModel.utilisateur = relationship("UtilisateurModel", foreign_keys="HistoriqueStatutModel.utilisateur_id")

# Relations pour FormationModel
FormationModel.candidat = relationship("UtilisateurModel", foreign_keys="FormationModel.candidat_id")

# Relations pour ExperienceModel
ExperienceModel.candidat = relationship("UtilisateurModel", foreign_keys="ExperienceModel.candidat_id")

__all__ = [
    "Base",
    "UtilisateurModel",
    "CandidatModel",
    "AdministrateurModel",
    "AdministrateurRHModel",
    "SuperAdministrateurModel",
    "OffreModel",
    "CandidatureModel",
    "DocumentModel",
    "NotificationModel",
    "HistoriqueStatutModel",
    "FormationModel",
    "ExperienceModel",
]