"""Value object pour les adresses email."""

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Email:
    """Adresse email validée."""

    valeur: str

    def __post_init__(self) -> None:
        """Valide l'adresse email à la création."""
        if not self.valeur:
            raise ValueError("L'adresse email ne peut pas être vide")

        if not self._est_valide(self.valeur):
            raise ValueError(f"Adresse email invalide: {self.valeur}")

    @staticmethod
    def _est_valide(email: str) -> bool:
        """Valide le format de l'adresse email."""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    def __str__(self) -> str:
        return self.valeur