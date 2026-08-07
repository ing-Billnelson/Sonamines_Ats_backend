"""Modèles SQLAlchemy pour les documents."""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Enum as SQLAEnum
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship

from ....domain.entities.document import TypeDocument
from .utilisateur_model import Base


class DocumentModel(Base):
    """Modèle SQLAlchemy pour la table documents."""

    __tablename__ = "documents"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Relations
    candidature_id = Column(PGUUID(as_uuid=True), ForeignKey("candidatures.id"), nullable=False)
    telechargeur_id = Column(PGUUID(as_uuid=True), ForeignKey("utilisateurs.id"), nullable=False)
    
    # Métadonnées du document
    type_document = Column(SQLAEnum(TypeDocument), nullable=False)
    nom_original = Column(String(255), nullable=False)
    nom_fichier_stockage = Column(String(255), nullable=False)
    url_stockage = Column(String(500), nullable=False)  # Clé MinIO
    taille_octets = Column(Integer, nullable=False)
    type_mime = Column(String(100), nullable=False)
    
    # Date
    date_telechargement = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<DocumentModel(id={self.id}, nom={self.nom_original})>"