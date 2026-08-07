"""Configuration de l'application avec pydantic-settings."""

from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration de l'application."""

    # Base de données
    database_url: str = Field(
        default="postgresql+asyncpg://sonamines:sonamines123@localhost:5432/sonamines_candidatures",
        description="URL de connexion à la base de données PostgreSQL"
    )

    # Elasticsearch
    elasticsearch_url: str = Field(
        default="http://localhost:9200",
        description="URL du serveur Elasticsearch"
    )

    # MinIO
    minio_endpoint: str = Field(
        default="localhost:9000",
        description="Endpoint du serveur MinIO"
    )
    minio_access_key: str = Field(
        default="admin",
        description="Clé d'accès MinIO"
    )
    minio_secret_key: str = Field(
        default="admin123",
        description="Clé secrète MinIO"
    )
    minio_bucket: str = Field(
        default="documents-candidatures",
        description="Nom du bucket MinIO"
    )
    minio_secure: bool = Field(
        default=False,
        description="Utiliser HTTPS pour MinIO"
    )

    # JWT
    jwt_secret_key: str = Field(
        default="your-super-secret-jwt-key-here-change-in-production",
        description="Clé secrète pour les tokens JWT"
    )
    jwt_algorithm: str = Field(
        default="HS256",
        description="Algorithme de chiffrement JWT"
    )
    jwt_access_token_expire_minutes: int = Field(
        default=30,
        description="Durée de validité des tokens d'accès (en minutes)"
    )

    # Contraintes fichiers
    max_taille_document_mo: int = Field(
        default=10,
        description="Taille maximum des documents en Mo"
    )
    max_taille_photo_mo: int = Field(
        default=2,
        description="Taille maximum des photos en Mo"
    )

    # Formats autorisés
    formats_documents_autorises: str = Field(
        default="pdf,doc,docx,jpg,jpeg,png",
        description="Formats de documents autorisés (séparés par des virgules)"
    )
    formats_photo_autorises: str = Field(
        default="jpg,jpeg,png",
        description="Formats de photos autorisés (séparés par des virgules)"
    )

    # Email
    smtp_host: str = Field(
        default="smtp.gmail.com",
        description="Serveur SMTP pour l'envoi d'emails"
    )
    smtp_port: int = Field(
        default=587,
        description="Port du serveur SMTP"
    )
    smtp_username: str = Field(
        default="",
        description="Nom d'utilisateur SMTP"
    )
    smtp_password: str = Field(
        default="",
        description="Mot de passe SMTP"
    )
    smtp_tls: bool = Field(
        default=True,
        description="Utiliser TLS pour SMTP"
    )

    # SMS
    sms_api_key: str = Field(
        default="",
        description="Clé API pour l'envoi de SMS"
    )
    sms_api_url: str = Field(
        default="",
        description="URL de l'API SMS"
    )

    # Logs
    log_level: str = Field(
        default="INFO",
        description="Niveau de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    @property
    def formats_documents_autorises_list(self) -> List[str]:
        """Retourne la liste des formats de documents autorisés."""
        return [fmt.strip().lower() for fmt in self.formats_documents_autorises.split(",")]

    @property
    def formats_photo_autorises_list(self) -> List[str]:
        """Retourne la liste des formats de photos autorisés."""
        return [fmt.strip().lower() for fmt in self.formats_photo_autorises.split(",")]

    @property
    def max_taille_document_octets(self) -> int:
        """Retourne la taille max des documents en octets."""
        return self.max_taille_document_mo * 1024 * 1024

    @property
    def max_taille_photo_octets(self) -> int:
        """Retourne la taille max des photos en octets."""
        return self.max_taille_photo_mo * 1024 * 1024


# Instance globale des paramètres
settings = Settings()