"""Modèle SQLAlchemy pour les expériences professionnelles."""

from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from .utilisateur_model import Base


class ExperienceModel(Base):
    """Modèle SQLAlchemy pour la table experiences."""

    __tablename__ = "experiences"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    candidat_id = Column(PGUUID(as_uuid=True), ForeignKey("utilisateurs.id"), nullable=False)
    entreprise = Column(String(255), nullable=False)
    poste = Column(String(255), nullable=False)
    date_debut = Column(DateTime, nullable=False)
    date_fin = Column(DateTime, nullable=True)
    description = Column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<ExperienceModel(id={self.id}, poste={self.poste})>"
