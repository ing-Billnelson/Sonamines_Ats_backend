"""Repository PostgreSQL pour les candidatures."""

from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func

from ....domain.entities import Candidature, Document, HistoriqueStatut
from ....domain.enums import StatutCandidature
from ....domain.ports import CandidatureRepository
from ....domain.value_objects import NumeroReference
from ..models import CandidatureModel, DocumentModel, HistoriqueStatutModel


class PostgresCandidatureRepository(CandidatureRepository):
    """Repository PostgreSQL pour la gestion des candidatures."""

    def __init__(self, session: AsyncSession):
        self._session = session

    def _model_vers_entite(self, model: CandidatureModel) -> Candidature:
        """Convertit un modèle SQLAlchemy en entité domaine."""
        return Candidature(
            id=model.id,
            numero_reference=NumeroReference(model.numero_reference),
            candidat_id=model.candidat_id,
            offre_id=model.offre_id,
            statut=model.statut,
            message_motivation=model.message_motivation,
            date_soumission=model.date_soumission,
            date_derniere_modification=model.date_derniere_modification,
            notes_internes=model.notes_internes,
            documents=[],
        )

    async def sauvegarder(self, candidature: Candidature) -> Candidature:
        """Sauvegarde une candidature et retourne l'entité mise à jour."""
        query = select(CandidatureModel).where(CandidatureModel.id == candidature.id)
        result = await self._session.execute(query)
        model = result.scalar_one_or_none()

        if model is None:
            model = CandidatureModel(
                id=candidature.id,
                numero_reference=str(candidature.numero_reference),
                candidat_id=candidature.candidat_id,
                offre_id=candidature.offre_id,
                statut=candidature.statut,
                message_motivation=candidature.message_motivation,
                date_soumission=candidature.date_soumission,
                date_derniere_modification=candidature.date_derniere_modification,
                notes_internes=candidature.notes_internes,
            )
            self._session.add(model)
        else:
            model.numero_reference = str(candidature.numero_reference)
            model.candidat_id = candidature.candidat_id
            model.offre_id = candidature.offre_id
            model.statut = candidature.statut
            model.message_motivation = candidature.message_motivation
            model.date_soumission = candidature.date_soumission
            model.date_derniere_modification = candidature.date_derniere_modification
            model.notes_internes = candidature.notes_internes

        await self._session.flush()
        return self._model_vers_entite(model)

    async def obtenir_par_id(self, candidature_id: UUID) -> Optional[Candidature]:
        """Récupère une candidature par son ID."""
        query = select(CandidatureModel).where(CandidatureModel.id == candidature_id)
        result = await self._session.execute(query)
        model = result.scalar_one_or_none()

        if not model:
            return None

        return self._model_vers_entite(model)

    async def obtenir_par_numero_reference(
        self, numero_reference: NumeroReference
    ) -> Optional[Candidature]:
        """Récupère une candidature par son numéro de référence."""
        query = select(CandidatureModel).where(
            CandidatureModel.numero_reference == str(numero_reference)
        )
        result = await self._session.execute(query)
        model = result.scalar_one_or_none()

        if not model:
            return None

        return self._model_vers_entite(model)

    async def lister_par_candidat(self, candidat_id: UUID) -> list[Candidature]:
        """Liste toutes les candidatures d'un candidat."""
        query = select(CandidatureModel).where(
            CandidatureModel.candidat_id == candidat_id
        )
        result = await self._session.execute(query)
        models = result.scalars().all()
        return [self._model_vers_entite(model) for model in models]

    async def lister_par_offre(self, offre_id: UUID) -> list[Candidature]:
        """Liste toutes les candidatures pour une offre."""
        # TODO: Implémenter la récupération et conversion
        return []

    async def lister_candidatures_spontanees(self) -> list[Candidature]:
        """Liste toutes les candidatures spontanées."""
        # TODO: Implémenter la récupération et conversion
        return []

    async def lister_toutes(
        self,
        statut: Optional[StatutCandidature] = None,
        offre_id: Optional[UUID] = None,
        spontanee: Optional[bool] = None,
        page: int = 1,
        taille_page: int = 20,
    ) -> tuple[list[Candidature], int]:
        """Liste les candidatures avec filtres optionnels et pagination."""
        conditions = []
        if statut is not None:
            conditions.append(CandidatureModel.statut == statut)
        if offre_id is not None:
            conditions.append(CandidatureModel.offre_id == offre_id)
        if spontanee is True:
            conditions.append(CandidatureModel.offre_id.is_(None))
        elif spontanee is False:
            conditions.append(CandidatureModel.offre_id.is_not(None))

        base_query = select(CandidatureModel)
        if conditions:
            base_query = base_query.where(*conditions)

        count_query = select(func.count()).select_from(CandidatureModel)
        if conditions:
            count_query = count_query.where(*conditions)
        total_result = await self._session.execute(count_query)
        total = total_result.scalar_one()

        result = await self._session.execute(
            base_query.limit(taille_page).offset((page - 1) * taille_page)
        )
        models = result.scalars().all()
        return [self._model_vers_entite(model) for model in models], total

    def _model_vers_entite_document(self, model: DocumentModel) -> Document:
        """Convertit un modèle SQLAlchemy document en entité domaine."""
        return Document(
            id=model.id,
            candidature_id=model.candidature_id,
            type_document=model.type_document,
            nom_original=model.nom_original,
            nom_fichier_stockage=model.nom_fichier_stockage,
            url_stockage=model.url_stockage,
            taille_octets=model.taille_octets,
            type_mime=model.type_mime,
            date_telechargement=model.date_telechargement,
            telechargeur_id=model.telechargeur_id,
        )

    async def sauvegarder_document(self, document: Document) -> Document:
        """Sauvegarde un document et retourne l'entité mise à jour."""
        query = select(DocumentModel).where(DocumentModel.id == document.id)
        result = await self._session.execute(query)
        model = result.scalar_one_or_none()

        if model is None:
            model = DocumentModel(
                id=document.id,
                candidature_id=document.candidature_id,
                telechargeur_id=document.telechargeur_id,
                type_document=document.type_document,
                nom_original=document.nom_original,
                nom_fichier_stockage=document.nom_fichier_stockage,
                url_stockage=document.url_stockage,
                taille_octets=document.taille_octets,
                type_mime=document.type_mime,
                date_telechargement=document.date_telechargement,
            )
            self._session.add(model)
        else:
            model.candidature_id = document.candidature_id
            model.telechargeur_id = document.telechargeur_id
            model.type_document = document.type_document
            model.nom_original = document.nom_original
            model.nom_fichier_stockage = document.nom_fichier_stockage
            model.url_stockage = document.url_stockage
            model.taille_octets = document.taille_octets
            model.type_mime = document.type_mime
            model.date_telechargement = document.date_telechargement

        await self._session.flush()
        return self._model_vers_entite_document(model)

    async def obtenir_documents_candidature(
        self, candidature_id: UUID
    ) -> list[Document]:
        """Récupère tous les documents d'une candidature."""
        query = (
            select(DocumentModel)
            .where(DocumentModel.candidature_id == candidature_id)
            .order_by(DocumentModel.date_telechargement)
        )
        result = await self._session.execute(query)
        models = result.scalars().all()
        return [self._model_vers_entite_document(model) for model in models]

    async def supprimer_document(self, document_id: UUID) -> bool:
        """Supprime un document du système."""
        query = delete(DocumentModel).where(DocumentModel.id == document_id)
        result = await self._session.execute(query)
        await self._session.flush()
        return result.rowcount > 0

    async def sauvegarder_historique_statut(
        self, historique: HistoriqueStatut
    ) -> HistoriqueStatut:
        """Sauvegarde un historique de statut (toujours un nouvel enregistrement)."""
        model = HistoriqueStatutModel(
            id=historique.id,
            candidature_id=historique.candidature_id,
            utilisateur_id=historique.utilisateur_id,
            ancien_statut=historique.ancien_statut,
            nouveau_statut=historique.nouveau_statut,
            commentaire=historique.commentaire,
            date_changement=historique.date_changement,
        )
        self._session.add(model)
        await self._session.flush()
        return historique

    async def obtenir_historique_candidature(
        self, candidature_id: UUID
    ) -> list[HistoriqueStatut]:
        """Récupère l'historique des statuts d'une candidature."""
        # TODO: Implémenter la récupération et conversion
        return []

    async def supprimer(self, candidature_id: UUID) -> bool:
        """Supprime une candidature du système."""
        # TODO: Implémenter la suppression
        return False