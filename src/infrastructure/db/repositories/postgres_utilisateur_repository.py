"""Repository PostgreSQL pour les utilisateurs."""

from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ....domain.entities import Candidat, AdministrateurRH, SuperAdministrateur, Utilisateur
from ....domain.ports import UtilisateurRepository
from ....domain.value_objects import Email
from ..models import (
    CandidatModel,
    AdministrateurRHModel,
    SuperAdministrateurModel,
    UtilisateurModel,
)


class PostgresUtilisateurRepository(UtilisateurRepository):
    """Repository PostgreSQL pour la gestion des utilisateurs."""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def sauvegarder_candidat(self, candidat: Candidat) -> Candidat:
        """Sauvegarde un candidat et retourne l'entité mise à jour."""
        # TODO: Implémenter la conversion entité -> modèle -> entité
        # Pour l'instant, stub qui retourne l'entité telle quelle
        return candidat

    async def sauvegarder_admin_rh(self, admin: AdministrateurRH) -> AdministrateurRH:
        """Sauvegarde un administrateur RH et retourne l'entité mise à jour."""
        # TODO: Implémenter la conversion entité -> modèle -> entité
        return admin

    async def sauvegarder_super_admin(
        self, admin: SuperAdministrateur
    ) -> SuperAdministrateur:
        """Sauvegarde un super administrateur et retourne l'entité mise à jour."""
        # TODO: Implémenter la conversion entité -> modèle -> entité
        return admin

    async def obtenir_par_id(self, utilisateur_id: UUID) -> Optional[Utilisateur]:
        """Récupère un utilisateur par son ID."""
        query = select(UtilisateurModel).where(UtilisateurModel.id == utilisateur_id)
        result = await self._session.execute(query)
        model = result.scalar_one_or_none()
        
        if not model:
            return None
        
        # TODO: Implémenter la conversion modèle -> entité
        return None

    async def obtenir_par_email(self, email: Email) -> Optional[Utilisateur]:
        """Récupère un utilisateur par son email."""
        query = select(UtilisateurModel).where(UtilisateurModel.email == str(email))
        result = await self._session.execute(query)
        model = result.scalar_one_or_none()
        
        if not model:
            return None
        
        # TODO: Implémenter la conversion modèle -> entité
        return None

    async def obtenir_candidat_par_id(self, candidat_id: UUID) -> Optional[Candidat]:
        """Récupère un candidat spécifiquement par son ID."""
        query = select(CandidatModel).where(CandidatModel.id == candidat_id)
        result = await self._session.execute(query)
        model = result.scalar_one_or_none()
        
        if not model:
            return None
        
        # TODO: Implémenter la conversion modèle -> entité
        return None

    async def obtenir_admin_rh_par_id(
        self, admin_id: UUID
    ) -> Optional[AdministrateurRH]:
        """Récupère un administrateur RH par son ID."""
        query = select(AdministrateurRHModel).where(AdministrateurRHModel.id == admin_id)
        result = await self._session.execute(query)
        model = result.scalar_one_or_none()
        
        if not model:
            return None
        
        # TODO: Implémenter la conversion modèle -> entité
        return None

    async def obtenir_super_admin_par_id(
        self, admin_id: UUID
    ) -> Optional[SuperAdministrateur]:
        """Récupère un super administrateur par son ID."""
        query = select(SuperAdministrateurModel).where(SuperAdministrateurModel.id == admin_id)
        result = await self._session.execute(query)
        model = result.scalar_one_or_none()
        
        if not model:
            return None
        
        # TODO: Implémenter la conversion modèle -> entité
        return None

    async def email_existe(self, email: Email) -> bool:
        """Vérifie si un email existe déjà dans le système."""
        query = select(UtilisateurModel.id).where(UtilisateurModel.email == str(email))
        result = await self._session.execute(query)
        return result.scalar_one_or_none() is not None

    async def supprimer(self, utilisateur_id: UUID) -> bool:
        """Supprime un utilisateur du système."""
        query = select(UtilisateurModel).where(UtilisateurModel.id == utilisateur_id)
        result = await self._session.execute(query)
        model = result.scalar_one_or_none()
        
        if not model:
            return False
        
        await self._session.delete(model)
        await self._session.commit()
        return True