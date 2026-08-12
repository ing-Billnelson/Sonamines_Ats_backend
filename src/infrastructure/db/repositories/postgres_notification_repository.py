"""Repository PostgreSQL pour les notifications."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, update

from ....domain.entities import Notification
from ....domain.ports import NotificationRepository
from ..models import NotificationModel


class PostgresNotificationRepository(NotificationRepository):
    """Repository PostgreSQL pour la gestion des notifications internes."""

    def __init__(self, session: AsyncSession):
        self._session = session

    def _model_vers_entite(self, model: NotificationModel) -> Notification:
        """Convertit un modèle SQLAlchemy en entité domaine."""
        return Notification(
            id=model.id,
            utilisateur_id=model.utilisateur_id,
            type_evenement=model.type_evenement,
            canal=model.canal,
            contenu=model.contenu,
            statut_lu=model.statut_lu,
            date_creation=model.date_creation,
            date_lecture=model.date_lecture,
        )

    async def sauvegarder(self, notification: Notification) -> Notification:
        """Sauvegarde une notification et retourne l'entité mise à jour."""
        query = select(NotificationModel).where(NotificationModel.id == notification.id)
        result = await self._session.execute(query)
        model = result.scalar_one_or_none()

        if model is None:
            model = NotificationModel(
                id=notification.id,
                utilisateur_id=notification.utilisateur_id,
                type_evenement=notification.type_evenement,
                canal=notification.canal,
                contenu=notification.contenu,
                statut_lu=notification.statut_lu,
                date_creation=notification.date_creation,
                date_lecture=notification.date_lecture,
            )
            self._session.add(model)
        else:
            model.utilisateur_id = notification.utilisateur_id
            model.type_evenement = notification.type_evenement
            model.canal = notification.canal
            model.contenu = notification.contenu
            model.statut_lu = notification.statut_lu
            model.date_creation = notification.date_creation
            model.date_lecture = notification.date_lecture

        await self._session.flush()
        return self._model_vers_entite(model)

    async def obtenir_par_id(self, notification_id: UUID) -> Optional[Notification]:
        """Récupère une notification par son ID."""
        query = select(NotificationModel).where(NotificationModel.id == notification_id)
        result = await self._session.execute(query)
        model = result.scalar_one_or_none()

        if not model:
            return None

        return self._model_vers_entite(model)

    async def lister_par_utilisateur(
        self, utilisateur_id: UUID, limit: int = 50, offset: int = 0
    ) -> list[Notification]:
        """Liste les notifications d'un utilisateur (paginé, plus récentes d'abord)."""
        query = (
            select(NotificationModel)
            .where(NotificationModel.utilisateur_id == utilisateur_id)
            .order_by(NotificationModel.date_creation.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self._session.execute(query)
        models = result.scalars().all()
        return [self._model_vers_entite(model) for model in models]

    async def lister_non_lues_par_utilisateur(
        self, utilisateur_id: UUID
    ) -> list[Notification]:
        """Liste les notifications non lues d'un utilisateur."""
        # TODO: Implémenter la récupération et conversion
        return []

    async def compter_non_lues_par_utilisateur(self, utilisateur_id: UUID) -> int:
        """Compte les notifications non lues d'un utilisateur."""
        query = (
            select(func.count())
            .select_from(NotificationModel)
            .where(
                NotificationModel.utilisateur_id == utilisateur_id,
                NotificationModel.statut_lu == False,  # noqa: E712
            )
        )
        result = await self._session.execute(query)
        return result.scalar_one()

    async def marquer_toutes_comme_lues(self, utilisateur_id: UUID) -> int:
        """Marque toutes les notifications non lues d'un utilisateur comme lues."""
        now = datetime.utcnow()
        query = (
            update(NotificationModel)
            .where(
                NotificationModel.utilisateur_id == utilisateur_id,
                NotificationModel.statut_lu == False,  # noqa: E712
            )
            .values(statut_lu=True, date_lecture=now)
        )
        result = await self._session.execute(query)
        await self._session.flush()
        return result.rowcount

    async def supprimer_anciennes(self, jours: int = 90) -> int:
        """Supprime les notifications anciennes (par défaut > 90 jours)."""
        # TODO: Implémenter la suppression en lot
        return 0