"""Modèles SQLAlchemy pour les utilisateurs."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime, String, Boolean, Enum as SQLAEnum
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.ext.declarative import declarative_base

from ....domain.enums import CanalNotification, StatutCompte

Base = declarative_base()


class UtilisateurModel(Base):
    """Modèle SQLAlchemy pour la table utilisateurs."""

    __tablename__ = "utilisateurs"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    telephone = Column(String(20), nullable=True)
    mot_de_passe_hash = Column(String(255), nullable=False)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    
    # Énums
    statut = Column(SQLAEnum(StatutCompte), nullable=False, default=StatutCompte.EN_ATTENTE_VALIDATION)
    canal_validation = Column(SQLAEnum(CanalNotification), nullable=False)
    
    # Flags de vérification
    email_verifie = Column(Boolean, nullable=False, default=False)
    telephone_verifie = Column(Boolean, nullable=False, default=False)
    
    # Dates
    date_creation = Column(DateTime, nullable=False, default=datetime.utcnow)
    date_derniere_connexion = Column(DateTime, nullable=True)
    date_modification = Column(DateTime, nullable=True)
    
    # Type d'utilisateur (discriminateur pour l'héritage)
    type_utilisateur = Column(String(50), nullable=False)
    
    # Champ spécifique aux candidats
    photo_url = Column(String(500), nullable=True)  # Seulement pour les candidats
    
    __mapper_args__ = {
        "polymorphic_identity": "utilisateur",
        "polymorphic_on": type_utilisateur,
        "with_polymorphic": "*",
    }

    def __repr__(self) -> str:
        return f"<UtilisateurModel(id={self.id}, email={self.email}, type={self.type_utilisateur})>"


class CandidatModel(UtilisateurModel):
    """Modèle SQLAlchemy pour les candidats."""

    __mapper_args__ = {
        "polymorphic_identity": "candidat",
    }


class AdministrateurModel(UtilisateurModel):
    """Modèle SQLAlchemy de base pour les administrateurs."""

    __mapper_args__ = {
        "polymorphic_identity": "administrateur",
    }


class AdministrateurRHModel(AdministrateurModel):
    """Modèle SQLAlchemy pour les administrateurs RH."""

    __mapper_args__ = {
        "polymorphic_identity": "administrateur_rh",
    }


class SuperAdministrateurModel(AdministrateurModel):
    """Modèle SQLAlchemy pour les super administrateurs."""

    __mapper_args__ = {
        "polymorphic_identity": "super_administrateur",
    }