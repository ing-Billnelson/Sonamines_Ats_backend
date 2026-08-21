"""Repository PostgreSQL pour les offres."""

from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ....domain.entities import Offre, StatutOffre
from ....domain.ports import OffreRepository
from ....domain.value_objects import NumeroReference
from ..models import OffreModel


class PostgresOffreRepository(OffreRepository):
    """Repository PostgreSQL pour la gestion des offres."""

    def __init__(self, session: AsyncSession):
        self._session = session

    def _model_vers_entite(self, model: OffreModel) -> Offre:
        """Convertit un modèle SQLAlchemy en entité domaine."""
        return Offre(
            id=model.id,
            numero_reference=NumeroReference(model.numero_reference),
            titre=model.titre,
            description=model.description,
            type_offre=model.type_offre,
            type_contrat=model.type_contrat,
            type_stage=model.type_stage,
            statut=model.statut,
            date_limite_candidature=model.date_limite_candidature,
            lieu=model.lieu,
            salaire_min=model.salaire_min,
            salaire_max=model.salaire_max,
            competences_requises=model.competences_requises,
            experience_requise=model.experience_requise,
            createur_id=model.createur_id,
            date_creation=model.date_creation,
            date_publication=model.date_publication,
            date_cloture=model.date_cloture,
            date_modification=model.date_modification,
            eligibilite_activee=model.eligibilite_activee,
            niveau_academique_minimum=model.niveau_academique_minimum,
            langues_requises=model.langues_requises,
            disponibilite_requise=model.disponibilite_requise,
        )

    async def sauvegarder(self, offre: Offre) -> Offre:
        """Sauvegarde une offre et retourne l'entité mise à jour."""
        query = select(OffreModel).where(OffreModel.id == offre.id)
        result = await self._session.execute(query)
        model = result.scalar_one_or_none()

        if model is None:
            model = OffreModel(
                id=offre.id,
                numero_reference=str(offre.numero_reference),
                titre=offre.titre,
                description=offre.description,
                type_offre=offre.type_offre,
                type_contrat=offre.type_contrat,
                type_stage=offre.type_stage,
                statut=offre.statut,
                date_limite_candidature=offre.date_limite_candidature,
                lieu=offre.lieu,
                salaire_min=offre.salaire_min,
                salaire_max=offre.salaire_max,
                competences_requises=offre.competences_requises,
                experience_requise=offre.experience_requise,
                createur_id=offre.createur_id,
                date_creation=offre.date_creation,
                date_publication=offre.date_publication,
                date_cloture=offre.date_cloture,
                date_modification=offre.date_modification,
                eligibilite_activee=offre.eligibilite_activee,
                niveau_academique_minimum=offre.niveau_academique_minimum,
                langues_requises=offre.langues_requises,
                disponibilite_requise=offre.disponibilite_requise,
            )
            self._session.add(model)
        else:
            model.numero_reference = str(offre.numero_reference)
            model.titre = offre.titre
            model.description = offre.description
            model.type_offre = offre.type_offre
            model.type_contrat = offre.type_contrat
            model.type_stage = offre.type_stage
            model.statut = offre.statut
            model.date_limite_candidature = offre.date_limite_candidature
            model.lieu = offre.lieu
            model.salaire_min = offre.salaire_min
            model.salaire_max = offre.salaire_max
            model.competences_requises = offre.competences_requises
            model.experience_requise = offre.experience_requise
            model.createur_id = offre.createur_id
            model.date_creation = offre.date_creation
            model.date_publication = offre.date_publication
            model.date_cloture = offre.date_cloture
            model.date_modification = offre.date_modification
            model.eligibilite_activee = offre.eligibilite_activee
            model.niveau_academique_minimum = offre.niveau_academique_minimum
            model.langues_requises = offre.langues_requises
            model.disponibilite_requise = offre.disponibilite_requise

        await self._session.flush()
        return self._model_vers_entite(model)

    async def obtenir_par_id(self, offre_id: UUID) -> Optional[Offre]:
        """Récupère une offre par son ID."""
        query = select(OffreModel).where(OffreModel.id == offre_id)
        result = await self._session.execute(query)
        model = result.scalar_one_or_none()

        if not model:
            return None

        return self._model_vers_entite(model)

    async def obtenir_par_numero_reference(
        self, numero_reference: NumeroReference
    ) -> Optional[Offre]:
        """Récupère une offre par son numéro de référence."""
        query = select(OffreModel).where(
            OffreModel.numero_reference == str(numero_reference)
        )
        result = await self._session.execute(query)
        model = result.scalar_one_or_none()

        if not model:
            return None

        return self._model_vers_entite(model)

    async def lister_offres_ouvertes(self) -> list[Offre]:
        """Liste toutes les offres ouvertes aux candidatures."""
        query = select(OffreModel).where(OffreModel.statut == StatutOffre.OUVERTE)
        result = await self._session.execute(query)
        models = result.scalars().all()
        return [self._model_vers_entite(model) for model in models]

    async def lister_offres_par_createur(self, createur_id: UUID) -> list[Offre]:
        """Liste toutes les offres créées par un administrateur RH."""
        query = select(OffreModel).where(OffreModel.createur_id == createur_id)
        result = await self._session.execute(query)
        models = result.scalars().all()
        return [self._model_vers_entite(model) for model in models]

    async def supprimer(self, offre_id: UUID) -> bool:
        """Supprime une offre du système."""
        # TODO: Implémenter la suppression
        return False