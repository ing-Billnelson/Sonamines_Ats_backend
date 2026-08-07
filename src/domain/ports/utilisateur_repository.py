"""Port repository pour la gestion des utilisateurs."""

from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from ..entities import AdministrateurRH, Candidat, SuperAdministrateur, Utilisateur
from ..value_objects import Email


class UtilisateurRepository(ABC):
    """Interface repository pour la gestion des utilisateurs."""

    @abstractmethod
    async def sauvegarder_candidat(self, candidat: Candidat) -> Candidat:
        """Sauvegarde un candidat et retourne l'entité mise à jour."""
        pass

    @abstractmethod
    async def sauvegarder_admin_rh(self, admin: AdministrateurRH) -> AdministrateurRH:
        """Sauvegarde un administrateur RH et retourne l'entité mise à jour."""
        pass

    @abstractmethod
    async def sauvegarder_super_admin(
        self, admin: SuperAdministrateur
    ) -> SuperAdministrateur:
        """Sauvegarde un super administrateur et retourne l'entité mise à jour."""
        pass

    @abstractmethod
    async def obtenir_par_id(self, utilisateur_id: UUID) -> Optional[Utilisateur]:
        """Récupère un utilisateur par son ID."""
        pass

    @abstractmethod
    async def obtenir_par_email(self, email: Email) -> Optional[Utilisateur]:
        """Récupère un utilisateur par son email."""
        pass

    @abstractmethod
    async def obtenir_candidat_par_id(self, candidat_id: UUID) -> Optional[Candidat]:
        """Récupère un candidat spécifiquement par son ID."""
        pass

    @abstractmethod
    async def obtenir_admin_rh_par_id(
        self, admin_id: UUID
    ) -> Optional[AdministrateurRH]:
        """Récupère un administrateur RH par son ID."""
        pass

    @abstractmethod
    async def obtenir_super_admin_par_id(
        self, admin_id: UUID
    ) -> Optional[SuperAdministrateur]:
        """Récupère un super administrateur par son ID."""
        pass

    @abstractmethod
    async def email_existe(self, email: Email) -> bool:
        """Vérifie si un email existe déjà dans le système."""
        pass

    @abstractmethod
    async def supprimer(self, utilisateur_id: UUID) -> bool:
        """Supprime un utilisateur du système."""
        pass