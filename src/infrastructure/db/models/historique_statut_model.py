"""Modèles SQLAlchemy pour l'historique des statuts."""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, String, Text, ForeignKey, Enum as SQLAEnum
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship

from ....domain.enums import StatutCandidature
from .utilisateur_model import Base


class HistoriqueStatutModel(Base):
    """Modèle SQLAlchemy pour la table historique_statuts."""

    __tablename__ = "historique_statuts"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Relations
    candidature_id = Column(PGUUID(as_uuid=True), ForeignKey("candidatures.id"), nullable=False)
    utilisateur_id = Column(PGUUID(as_uuid=True), ForeignKey("utilisateurs.id"), nullable=False)
    
    # Changement de statut
    ancien_statut = Column(SQLAEnum(StatutCandidature), nullable=True)  # None pour création initiale
    nouveau_statut = Column(SQLAEnum(StatutCandidature), nullable=False)
    commentaire = Column(Text, nullable=True)
    
    # Date
    date_changement = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<HistoriqueStatutModel(id={self.id}, {self.ancien_statut} -> {self.nouveau_statut})>"