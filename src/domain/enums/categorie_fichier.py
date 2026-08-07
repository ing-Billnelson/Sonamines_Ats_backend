"""Énumération des catégories de fichiers pour le stockage."""

from enum import Enum


class CategorieFichier(str, Enum):
    """Catégories de fichiers avec des règles de validation différentes."""

    DOCUMENT = "DOCUMENT"  # CV, lettres, diplômes, CNI, attestations
    PHOTO = "PHOTO"  # Photo de profil du candidat

    def __str__(self) -> str:
        return self.value