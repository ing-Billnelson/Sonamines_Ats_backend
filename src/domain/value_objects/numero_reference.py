"""Value object pour les numéros de référence."""

import uuid
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class NumeroReference:
    """Numéro de référence unique pour les candidatures et offres."""

    valeur: str

    def __post_init__(self) -> None:
        """Valide le numéro de référence à la création."""
        if not self.valeur:
            raise ValueError("Le numéro de référence ne peut pas être vide")

        if len(self.valeur) < 3:
            raise ValueError("Le numéro de référence doit contenir au moins 3 caractères")

    @classmethod
    def generer_candidature(cls) -> "NumeroReference":
        """Génère un numéro de référence pour une candidature."""
        annee = datetime.now().year
        uuid_court = str(uuid.uuid4())[:8].upper()
        return cls(f"CAND-{annee}-{uuid_court}")

    @classmethod
    def generer_offre(cls, type_offre: str) -> "NumeroReference":
        """Génère un numéro de référence pour une offre."""
        annee = datetime.now().year
        uuid_court = str(uuid.uuid4())[:8].upper()
        prefix = "EMPLOI" if type_offre == "EMPLOI" else "STAGE"
        return cls(f"{prefix}-{annee}-{uuid_court}")

    def __str__(self) -> str:
        return self.valeur