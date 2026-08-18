"""Entité formation."""

from dataclasses import dataclass
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Formation:
    """Entité représentant une formation d'un candidat."""

    id: UUID
    candidat_id: UUID
    etablissement: str
    diplome: str
    annee_debut: int
    annee_fin: Optional[int] = None

    @classmethod
    def creer_nouvelle(
        cls,
        candidat_id: UUID,
        etablissement: str,
        diplome: str,
        annee_debut: int,
        annee_fin: Optional[int] = None,
    ) -> "Formation":
        """Crée une nouvelle formation."""
        return cls(
            id=uuid4(),
            candidat_id=candidat_id,
            etablissement=etablissement,
            diplome=diplome,
            annee_debut=annee_debut,
            annee_fin=annee_fin,
        )
