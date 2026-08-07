"""Entité historique des changements de statut."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from ..enums import StatutCandidature


@dataclass
class HistoriqueStatut:
    """Entité représentant l'historique des changements de statut d'une candidature."""

    id: UUID
    candidature_id: UUID
    ancien_statut: Optional[StatutCandidature]
    nouveau_statut: StatutCandidature
    commentaire: Optional[str]
    utilisateur_id: UUID  # ID de l'utilisateur qui a effectué le changement
    date_changement: datetime

    @classmethod
    def creer_nouveau(
        cls,
        candidature_id: UUID,
        ancien_statut: Optional[StatutCandidature],
        nouveau_statut: StatutCandidature,
        utilisateur_id: UUID,
        commentaire: Optional[str] = None,
    ) -> "HistoriqueStatut":
        """Crée un nouvel enregistrement d'historique."""
        return cls(
            id=uuid4(),
            candidature_id=candidature_id,
            ancien_statut=ancien_statut,
            nouveau_statut=nouveau_statut,
            commentaire=commentaire,
            utilisateur_id=utilisateur_id,
            date_changement=datetime.utcnow(),
        )

    def est_creation_initiale(self) -> bool:
        """Vérifie si cet historique correspond à la création initiale."""
        return self.ancien_statut is None