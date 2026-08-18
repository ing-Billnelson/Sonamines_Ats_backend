"""Modèle SQLAlchemy pour les formations."""

from uuid import uuid4

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from .utilisateur_model import Base


class FormationModel(Base):
    """Modèle SQLAlchemy pour la table formations."""

    __tablename__ = "formations"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    candidat_id = Column(PGUUID(as_uuid=True), ForeignKey("utilisateurs.id"), nullable=False)
    etablissement = Column(String(255), nullable=False)
    diplome = Column(String(255), nullable=False)
    annee_debut = Column(Integer, nullable=False)
    annee_fin = Column(Integer, nullable=True)

    def __repr__(self) -> str:
        return f"<FormationModel(id={self.id}, diplome={self.diplome})>"
