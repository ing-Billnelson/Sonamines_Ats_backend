"""Modèles SQLAlchemy pour les candidatures."""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, String, Text, ForeignKey, Enum as SQLAEnum
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship

from ....domain.enums import StatutCandidature
from .utilisateur_model import Base


class CandidatureModel(Base):
    """Modèle SQLAlchemy pour la table candidatures."""

    __tablename__ = "candidatures"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    numero_reference = Column(String(50), unique=True, nullable=False, index=True)
    
    # Relations
    candidat_id = Column(PGUUID(as_uuid=True), ForeignKey("utilisateurs.id"), nullable=False)
    offre_id = Column(PGUUID(as_uuid=True), ForeignKey("offres.id"), nullable=True)  # None = spontanée
    
    # Statut et contenu
    statut = Column(SQLAEnum(StatutCandidature), nullable=False, default=StatutCandidature.RECUE)
    message_motivation = Column(Text, nullable=False)
    notes_internes = Column(Text, nullable=True)  # Notes des RH
    
    # Dates
    date_soumission = Column(DateTime, nullable=False, default=datetime.utcnow)
    date_derniere_modification = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<CandidatureModel(id={self.id}, statut={self.statut})>"