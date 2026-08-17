"""Adapter MinIO pour le stockage de fichiers."""

import mimetypes
from pathlib import Path
from typing import List
from uuid import UUID

from minio import Minio
from minio.error import S3Error

from ...domain.enums import CategorieFichier
from ...domain.exceptions import (
    FichierTropVolumineuxError,
    FormatFichierNonSupporteError,
)
from ...domain.ports import StoragePort
from ..config import Settings


class MinioAdapter(StoragePort):
    """Adapter MinIO pour le stockage de fichiers."""

    def __init__(self, settings: Settings):
        self._settings = settings
        self._client = Minio(
            endpoint=settings.minio_endpoint,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
            secure=settings.minio_secure,
        )
        self._bucket_name = settings.minio_bucket

    async def verifier_ou_creer_bucket(self) -> None:
        """
        Vérifie que le bucket existe, et le crée sinon.

        Idempotent : peut être appelé au démarrage de l'application et en
        filet de sécurité avant le premier téléversement. N'est pas bloquant
        si MinIO est indisponible (le bucket sera recréé plus tard).
        """
        try:
            if not self._client.bucket_exists(self._bucket_name):
                self._client.make_bucket(self._bucket_name)
        except S3Error:
            return

    async def televerser(
        self,
        fichier: bytes,
        nom_original: str,
        categorie: CategorieFichier,
        proprietaire_id: UUID,
    ) -> str:
        """
        Téléverse un fichier dans MinIO.

        Args:
            fichier: Contenu binaire du fichier
            nom_original: Nom original du fichier
            categorie: Catégorie du fichier (DOCUMENT ou PHOTO)
            proprietaire_id: ID du propriétaire du fichier

        Returns:
            URL/clé de stockage du fichier

        Raises:
            FichierTropVolumineuxError: Si le fichier dépasse la taille autorisée
            FormatFichierNonSupporteError: Si le format n'est pas supporté
        """
        # Valider la taille du fichier
        taille_max = self.obtenir_taille_max_categorie(categorie)
        if len(fichier) > taille_max:
            raise FichierTropVolumineuxError(
                len(fichier), taille_max, categorie.value
            )

        # Valider le format du fichier
        extension = Path(nom_original).suffix.lower().lstrip(".")
        formats_autorises = self.obtenir_formats_autorises_categorie(categorie)
        if extension not in formats_autorises:
            raise FormatFichierNonSupporteError(
                extension, formats_autorises, categorie.value
            )

        # Générer le chemin de stockage
        chemin_stockage = self._generer_chemin_stockage(
            nom_original, categorie, proprietaire_id
        )

        try:
            # Filet de sécurité : s'assurer que le bucket existe
            await self.verifier_ou_creer_bucket()

            # Déterminer le type MIME
            type_mime, _ = mimetypes.guess_type(nom_original)
            if not type_mime:
                type_mime = "application/octet-stream"

            # Téléverser le fichier
            from io import BytesIO
            fichier_stream = BytesIO(fichier)

            self._client.put_object(
                bucket_name=self._bucket_name,
                object_name=chemin_stockage,
                data=fichier_stream,
                length=len(fichier),
                content_type=type_mime,
            )

            return chemin_stockage

        except S3Error as e:
            raise ValueError(f"Erreur lors du téléversement: {e}")

    async def supprimer(self, url_stockage: str, categorie: CategorieFichier) -> bool:
        """Supprime un fichier de MinIO."""
        try:
            self._client.remove_object(
                bucket_name=self._bucket_name,
                object_name=url_stockage,
            )
            return True
        except S3Error:
            return False

    async def generer_url_temporaire(
        self, url_stockage: str, duree_secondes: int = 3600
    ) -> str:
        """Génère une URL temporaire d'accès au fichier."""
        try:
            from datetime import timedelta
            url = self._client.presigned_get_object(
                bucket_name=self._bucket_name,
                object_name=url_stockage,
                expires=timedelta(seconds=duree_secondes),
            )
            return url
        except S3Error as e:
            raise ValueError(f"Erreur lors de la génération d'URL: {e}")

    async def verifier_existence(self, url_stockage: str) -> bool:
        """Vérifie si un fichier existe dans MinIO."""
        try:
            self._client.stat_object(
                bucket_name=self._bucket_name,
                object_name=url_stockage,
            )
            return True
        except S3Error:
            return False

    async def obtenir_taille_fichier(self, url_stockage: str) -> int:
        """Retourne la taille d'un fichier en octets."""
        try:
            stat = self._client.stat_object(
                bucket_name=self._bucket_name,
                object_name=url_stockage,
            )
            return stat.size
        except S3Error as e:
            raise ValueError(f"Erreur lors de la récupération de la taille: {e}")

    def obtenir_taille_max_categorie(self, categorie: CategorieFichier) -> int:
        """Retourne la taille maximum autorisée pour une catégorie."""
        if categorie == CategorieFichier.DOCUMENT:
            return self._settings.max_taille_document_octets
        elif categorie == CategorieFichier.PHOTO:
            return self._settings.max_taille_photo_octets
        else:
            raise ValueError(f"Catégorie inconnue: {categorie}")

    def obtenir_formats_autorises_categorie(
        self, categorie: CategorieFichier
    ) -> List[str]:
        """Retourne la liste des formats autorisés pour une catégorie."""
        if categorie == CategorieFichier.DOCUMENT:
            return self._settings.formats_documents_autorises_list
        elif categorie == CategorieFichier.PHOTO:
            return self._settings.formats_photo_autorises_list
        else:
            raise ValueError(f"Catégorie inconnue: {categorie}")

    def _generer_chemin_stockage(
        self, nom_original: str, categorie: CategorieFichier, proprietaire_id: UUID
    ) -> str:
        """Génère le chemin de stockage pour un fichier."""
        import time
        from pathlib import Path

        # Préfixe selon la catégorie
        prefixe = "documents" if categorie == CategorieFichier.DOCUMENT else "photos"

        # Extension du fichier
        extension = Path(nom_original).suffix

        # Timestamp pour unicité
        timestamp = int(time.time() * 1000)

        # Chemin final: {prefixe}/{proprietaire_id}/{timestamp}{extension}
        return f"{prefixe}/{proprietaire_id}/{timestamp}{extension}"