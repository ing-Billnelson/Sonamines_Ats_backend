"""Modèles SQLAlchemy pour les offres."""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, String, Text, Float, ARRAY, ForeignKey, Enum as SQLAEnum
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship

from ....domain.entities.offre import StatutOffre
from ....domain.enums import TypeContrat, TypeOffre, TypeStage
from .utilisateur_model import Base


class OffreModel(Base):
    """Modèle SQLAlchemy pour la table offres."""

    __tablename__ = "offres"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    numero_reference = Column(String(50), unique=True, nullable=False, index=True)
    titre = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    
    # Types et statuts
    type_offre = Column(SQLAEnum(TypeOffre), nullable=False)
    type_contrat = Column(SQLAEnum(TypeContrat), nullable=True)  # Seulement pour EMPLOI
    type_stage = Column(SQLAEnum(TypeStage), nullable=True)      # Seulement pour STAGE
    statut = Column(SQLAEnum(StatutOffre), nullable=False, default="BROUILLON")
    
    # Informations de l'offre
    lieu = Column(String(100), nullable=False)
    salaire_min = Column(Float, nullable=True)
    salaire_max = Column(Float, nullable=True)
    competences_requises = Column(ARRAY(String), nullable=False, default=list)
    experience_requise = Column(Text, nullable=True)
    
    # Dates
    date_limite_candidature = Column(DateTime, nullable=True)
    date_creation = Column(DateTime, nullable=False, default=datetime.utcnow)
    date_publication = Column(DateTime, nullable=True)
    date_cloture = Column(DateTime, nullable=True)
    date_modification = Column(DateTime, nullable=True)
    
    # Relations
    createur_id = Column(PGUUID(as_uuid=True), ForeignKey("utilisateurs.id"), nullable=False)

    def __repr__(self) -> str:
        return f"<OffreModel(id={self.id}, titre={self.titre}, statut={self.statut})>"