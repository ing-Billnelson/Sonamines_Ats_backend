"""Modèles SQLAlchemy pour les notifications."""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, String, Text, Boolean, ForeignKey, Enum as SQLAEnum
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship

from ....domain.enums import CanalNotification, TypeEvenement
from .utilisateur_model import Base


class NotificationModel(Base):
    """Modèle SQLAlchemy pour la table notifications."""

    __tablename__ = "notifications"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Relation
    utilisateur_id = Column(PGUUID(as_uuid=True), ForeignKey("utilisateurs.id"), nullable=False)
    
    # Contenu de la notification
    type_evenement = Column(SQLAEnum(TypeEvenement), nullable=False)
    canal = Column(SQLAEnum(CanalNotification), nullable=False, default=CanalNotification.INTERNE)
    contenu = Column(Text, nullable=False)
    
    # État de lecture
    statut_lu = Column(Boolean, nullable=False, default=False)
    
    # Dates
    date_creation = Column(DateTime, nullable=False, default=datetime.utcnow)
    date_lecture = Column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return f"<NotificationModel(id={self.id}, type={self.type_evenement}, lu={self.statut_lu})>"