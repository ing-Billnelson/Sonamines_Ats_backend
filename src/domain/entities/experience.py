"""Entité expérience professionnelle."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Experience:
    """Entité représentant une expérience professionnelle d'un candidat."""

    id: UUID
    candidat_id: UUID
    entreprise: str
    poste: str
    date_debut: datetime
    date_fin: Optional[datetime] = None
    description: Optional[str] = None

    @classmethod
    def creer_nouvelle(
        cls,
        candidat_id: UUID,
        entreprise: str,
        poste: str,
        date_debut: datetime,
        date_fin: Optional[datetime] = None,
        description: Optional[str] = None,
    ) -> "Experience":
        """Crée une nouvelle expérience professionnelle."""
        return cls(
            id=uuid4(),
            candidat_id=candidat_id,
            entreprise=entreprise,
            poste=poste,
            date_debut=date_debut,
            date_fin=date_fin,
            description=description,
        )
