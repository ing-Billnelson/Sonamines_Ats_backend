"""Repository PostgreSQL pour le profil candidat (formations et expériences)."""

from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from ....domain.entities import Experience, Formation
from ....domain.ports import ProfilCandidatRepository
from ..models import ExperienceModel, FormationModel


class PostgresProfilCandidatRepository(ProfilCandidatRepository):
    """Repository PostgreSQL pour les formations et expériences d'un candidat."""

    def __init__(self, session: AsyncSession):
        self._session = session

    def _formation_modele_vers_entite(self, model: FormationModel) -> Formation:
        """Convertit un modèle formation en entité domaine."""
        return Formation(
            id=model.id,
            candidat_id=model.candidat_id,
            etablissement=model.etablissement,
            diplome=model.diplome,
            annee_debut=model.annee_debut,
            annee_fin=model.annee_fin,
        )

    def _experience_modele_vers_entite(self, model: ExperienceModel) -> Experience:
        """Convertit un modèle expérience en entité domaine."""
        return Experience(
            id=model.id,
            candidat_id=model.candidat_id,
            entreprise=model.entreprise,
            poste=model.poste,
            date_debut=model.date_debut,
            date_fin=model.date_fin,
            description=model.description,
        )

    async def sauvegarder_formation(self, formation: Formation) -> Formation:
        """Sauvegarde une formation et retourne l'entité mise à jour."""
        model = FormationModel(
            id=formation.id,
            candidat_id=formation.candidat_id,
            etablissement=formation.etablissement,
            diplome=formation.diplome,
            annee_debut=formation.annee_debut,
            annee_fin=formation.annee_fin,
        )
        self._session.add(model)
        await self._session.flush()
        return self._formation_modele_vers_entite(model)

    async def obtenir_formations_candidat(self, candidat_id: UUID) -> list[Formation]:
        """Récupère les formations d'un candidat."""
        query = (
            select(FormationModel)
            .where(FormationModel.candidat_id == candidat_id)
            .order_by(FormationModel.annee_debut)
        )
        result = await self._session.execute(query)
        models = result.scalars().all()
        return [self._formation_modele_vers_entite(model) for model in models]

    async def supprimer_formation(self, formation_id: UUID) -> bool:
        """Supprime une formation. Retourne False si absente."""
        query = select(FormationModel.id).where(FormationModel.id == formation_id)
        result = await self._session.execute(query)
        if result.scalar_one_or_none() is None:
            return False

        await self._session.execute(
            delete(FormationModel).where(FormationModel.id == formation_id)
        )
        await self._session.flush()
        return True

    async def sauvegarder_experience(self, experience: Experience) -> Experience:
        """Sauvegarde une expérience et retourne l'entité mise à jour."""
        model = ExperienceModel(
            id=experience.id,
            candidat_id=experience.candidat_id,
            entreprise=experience.entreprise,
            poste=experience.poste,
            date_debut=experience.date_debut,
            date_fin=experience.date_fin,
            description=experience.description,
        )
        self._session.add(model)
        await self._session.flush()
        return self._experience_modele_vers_entite(model)

    async def obtenir_experiences_candidat(self, candidat_id: UUID) -> list[Experience]:
        """Récupère les expériences d'un candidat."""
        query = (
            select(ExperienceModel)
            .where(ExperienceModel.candidat_id == candidat_id)
            .order_by(ExperienceModel.date_debut.desc())
        )
        result = await self._session.execute(query)
        models = result.scalars().all()
        return [self._experience_modele_vers_entite(model) for model in models]

    async def supprimer_experience(self, experience_id: UUID) -> bool:
        """Supprime une expérience. Retourne False si absente."""
        query = select(ExperienceModel.id).where(ExperienceModel.id == experience_id)
        result = await self._session.execute(query)
        if result.scalar_one_or_none() is None:
            return False

        await self._session.execute(
            delete(ExperienceModel).where(ExperienceModel.id == experience_id)
        )
        await self._session.flush()
        return True
