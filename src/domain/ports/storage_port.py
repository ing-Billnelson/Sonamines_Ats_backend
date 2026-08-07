"""Port pour le stockage de fichiers avec MinIO."""

from abc import ABC, abstractmethod
from uuid import UUID

from ..enums import CategorieFichier


class StoragePort(ABC):
    """Interface pour le stockage de fichiers."""

    @abstractmethod
    async def televerser(
        self,
        fichier: bytes,
        nom_original: str,
        categorie: CategorieFichier,
        proprietaire_id: UUID,
    ) -> str:
        """
        Téléverse un fichier et retourne son URL de stockage.

        Args:
            fichier: Contenu binaire du fichier
            nom_original: Nom original du fichier
            categorie: Catégorie du fichier (DOCUMENT ou PHOTO)
            proprietaire_id: ID du propriétaire du fichier

        Returns:
            URL/clé de stockage du fichier téléversé

        Raises:
            FichierTropVolumineuxError: Si le fichier dépasse la taille autorisée
            FormatFichierNonSupporteError: Si le format n'est pas supporté
        """
        pass

    @abstractmethod
    async def supprimer(self, url_stockage: str, categorie: CategorieFichier) -> bool:
        """
        Supprime un fichier du stockage.

        Args:
            url_stockage: URL/clé de stockage du fichier
            categorie: Catégorie du fichier (pour localiser le bon bucket/préfixe)

        Returns:
            True si la suppression a réussi, False sinon
        """
        pass

    @abstractmethod
    async def generer_url_temporaire(
        self, url_stockage: str, duree_secondes: int = 3600
    ) -> str:
        """
        Génère une URL temporaire d'accès au fichier.

        Args:
            url_stockage: URL/clé de stockage du fichier
            duree_secondes: Durée de validité de l'URL (défaut: 1 heure)

        Returns:
            URL temporaire d'accès au fichier
        """
        pass

    @abstractmethod
    async def verifier_existence(self, url_stockage: str) -> bool:
        """Vérifie si un fichier existe dans le stockage."""
        pass

    @abstractmethod
    async def obtenir_taille_fichier(self, url_stockage: str) -> int:
        """Retourne la taille d'un fichier en octets."""
        pass

    @abstractmethod
    def obtenir_taille_max_categorie(self, categorie: CategorieFichier) -> int:
        """Retourne la taille maximum autorisée pour une catégorie (en octets)."""
        pass

    @abstractmethod
    def obtenir_formats_autorises_categorie(
        self, categorie: CategorieFichier
    ) -> list[str]:
        """Retourne la liste des formats autorisés pour une catégorie."""
        pass