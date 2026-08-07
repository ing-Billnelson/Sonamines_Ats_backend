"""Value object pour les numéros de téléphone."""

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class NumeroTelephone:
    """Numéro de téléphone validé."""

    valeur: str

    def __post_init__(self) -> None:
        """Valide le numéro de téléphone à la création."""
        if not self.valeur:
            raise ValueError("Le numéro de téléphone ne peut pas être vide")

        if not self._est_valide(self.valeur):
            raise ValueError(f"Numéro de téléphone invalide: {self.valeur}")

    @staticmethod
    def _est_valide(numero: str) -> bool:
        """Valide le format du numéro de téléphone."""
        # Supprime tous les espaces et caractères spéciaux
        numero_nettoye = re.sub(r"[^\d+]", "", numero)

        # Vérifie que le numéro commence par + ou contient au moins 8 chiffres
        if numero_nettoye.startswith("+"):
            return len(numero_nettoye) >= 10  # +XXX au minimum + 7 chiffres
        else:
            return len(numero_nettoye) >= 8  # Au minimum 8 chiffres

    def __str__(self) -> str:
        return self.valeur