"""Entité notification."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from ..enums import CanalNotification, TypeEvenement


@dataclass
class Notification:
    """Entité représentant une notification interne à la plateforme."""

    id: UUID
    utilisateur_id: UUID
    type_evenement: TypeEvenement
    canal: CanalNotification  # Toujours INTERNE pour les notifications persistées
    contenu: str
    statut_lu: bool
    date_creation: datetime
    date_lecture: Optional[datetime] = None

    @classmethod
    def creer_nouvelle(
        cls,
        utilisateur_id: UUID,
        type_evenement: TypeEvenement,
        contenu: str,
    ) -> "Notification":
        """Crée une nouvelle notification interne."""
        return cls(
            id=uuid4(),
            utilisateur_id=utilisateur_id,
            type_evenement=type_evenement,
            canal=CanalNotification.INTERNE,  # Toujours interne pour la persistance
            contenu=contenu,
            statut_lu=False,
            date_creation=datetime.utcnow(),
        )

    def marquer_comme_lue(self) -> None:
        """Marque la notification comme lue."""
        if not self.statut_lu:
            self.statut_lu = True
            self.date_lecture = datetime.utcnow()

    def marquer_comme_non_lue(self) -> None:
        """Marque la notification comme non lue."""
        if self.statut_lu:
            self.statut_lu = False
            self.date_lecture = None