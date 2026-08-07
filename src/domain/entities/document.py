"""Entité document."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4


class TypeDocument(str, Enum):
    """Types de documents acceptés dans un dossier de candidature."""

    CV = "CV"
    LETTRE_MOTIVATION = "LETTRE_MOTIVATION"
    DIPLOME = "DIPLOME"
    CNI = "CNI"
    ATTESTATION = "ATTESTATION"
    AUTRE = "AUTRE"

    def __str__(self) -> str:
        return self.value

    @property
    def is_obligatoire(self) -> bool:
        """Vérifie si le document est obligatoire par défaut."""
        return self in {TypeDocument.CV, TypeDocument.LETTRE_MOTIVATION}


@dataclass
class Document:
    """Entité représentant un document dans un dossier de candidature."""

    id: UUID
    candidature_id: UUID
    type_document: TypeDocument
    nom_original: str
    nom_fichier_stockage: str  # Nom du fichier dans le système de stockage
    url_stockage: str  # URL ou clé de stockage MinIO
    taille_octets: int
    type_mime: str
    date_telechargement: datetime
    telechargeur_id: UUID  # ID de l'utilisateur qui a téléchargé le document

    @classmethod
    def creer_nouveau(
        cls,
        candidature_id: UUID,
        type_document: TypeDocument,
        nom_original: str,
        nom_fichier_stockage: str,
        url_stockage: str,
        taille_octets: int,
        type_mime: str,
        telechargeur_id: UUID,
    ) -> "Document":
        """Crée un nouveau document."""
        return cls(
            id=uuid4(),
            candidature_id=candidature_id,
            type_document=type_document,
            nom_original=nom_original,
            nom_fichier_stockage=nom_fichier_stockage,
            url_stockage=url_stockage,
            taille_octets=taille_octets,
            type_mime=type_mime,
            date_telechargement=datetime.utcnow(),
            telechargeur_id=telechargeur_id,
        )

    def est_image(self) -> bool:
        """Vérifie si le document est une image."""
        return self.type_mime.startswith("image/")

    def est_pdf(self) -> bool:
        """Vérifie si le document est un PDF."""
        return self.type_mime == "application/pdf"