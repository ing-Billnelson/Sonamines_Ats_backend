"""Use case pour obtenir les détails complets d'une candidature (côté RH)."""

from uuid import UUID

from ...domain.exceptions import CandidatureIntrouvableError
from ...domain.ports import (
    CandidatureRepository,
    OffreRepository,
    StoragePort,
    UtilisateurRepository,
)
from ..dto import CandidatureDTO, DocumentDTO, HistoriqueStatutDTO


class ObtenirCandidatureRHUseCase:
    """Use case pour récupérer une candidature avec documents et historique."""

    def __init__(
        self,
        candidature_repository: CandidatureRepository,
        utilisateur_repository: UtilisateurRepository,
        offre_repository: OffreRepository,
        storage_port: StoragePort,
    ):
        self._candidature_repository = candidature_repository
        self._utilisateur_repository = utilisateur_repository
        self._offre_repository = offre_repository
        self._storage_port = storage_port

    async def executer(self, candidature_id: str) -> CandidatureDTO:
        """Récupère une candidature complète (RH).

        Args:
            candidature_id: UUID de la candidature (en string)

        Raises:
            CandidatureIntrouvableError: Si la candidature n'existe pas
        """
        candidature_uuid = UUID(candidature_id)

        candidature = await self._candidature_repository.obtenir_par_id(
            candidature_uuid
        )
        if candidature is None:
            raise CandidatureIntrouvableError(candidature_id)

        # Résolution candidat (nom complet + email)
        candidat_nom_complet = ""
        candidat_email = ""
        candidat = await self._utilisateur_repository.obtenir_candidat_par_id(
            candidature.candidat_id
        )
        if candidat is not None:
            candidat_nom_complet = candidat.nom_complet
            candidat_email = str(candidat.email)

        # Résolution offre (titre + référence)
        offre_titre = None
        offre_numero_reference = None
        if candidature.offre_id is not None:
            offre = await self._offre_repository.obtenir_par_id(candidature.offre_id)
            if offre is not None:
                offre_titre = offre.titre
                offre_numero_reference = str(offre.numero_reference)

        # Documents avec URL temporaire
        documents = await self._candidature_repository.obtenir_documents_candidature(
            candidature_uuid
        )
        documents_dto = [
            await self._convertir_document_en_dto(document) for document in documents
        ]

        # Historique des statuts
        historique = await self._candidature_repository.obtenir_historique_candidature(
            candidature_uuid
        )
        historique_dto = [
            await self._convertir_historique_en_dto(entry) for entry in historique
        ]

        return CandidatureDTO(
            id=str(candidature.id),
            numero_reference=str(candidature.numero_reference),
            candidat_nom_complet=candidat_nom_complet,
            candidat_email=candidat_email,
            offre_titre=offre_titre,
            offre_numero_reference=offre_numero_reference,
            statut=candidature.statut,
            message_motivation=candidature.message_motivation,
            notes_internes=candidature.notes_internes,
            date_soumission=candidature.date_soumission.isoformat(),
            date_derniere_modification=candidature.date_derniere_modification.isoformat(),
            documents=documents_dto,
            historique=historique_dto,
            est_spontanee=candidature.est_spontanee(),
            est_complete=candidature.est_complete(),
        )

    async def _convertir_document_en_dto(self, document) -> DocumentDTO:
        """Convertit un document en DTO avec URL temporaire."""
        url_temporaire = await self._storage_port.generer_url_temporaire(
            document.url_stockage
        )

        telechargeur_nom_complet = ""
        telechargeur = await self._utilisateur_repository.obtenir_par_id(
            document.telechargeur_id
        )
        if telechargeur is not None:
            telechargeur_nom_complet = telechargeur.nom_complet

        return DocumentDTO(
            id=str(document.id),
            type_document=document.type_document,
            nom_original=document.nom_original,
            taille_octets=document.taille_octets,
            type_mime=document.type_mime,
            url_temporaire=url_temporaire,
            date_telechargement=document.date_telechargement.isoformat(),
            telechargeur_nom_complet=telechargeur_nom_complet,
        )

    async def _convertir_historique_en_dto(
        self, entry
    ) -> HistoriqueStatutDTO:
        """Convertit un historique de statut en DTO."""
        utilisateur_nom_complet = ""
        utilisateur = await self._utilisateur_repository.obtenir_par_id(
            entry.utilisateur_id
        )
        if utilisateur is not None:
            utilisateur_nom_complet = utilisateur.nom_complet

        return HistoriqueStatutDTO(
            id=str(entry.id),
            ancien_statut=entry.ancien_statut,
            nouveau_statut=entry.nouveau_statut,
            commentaire=entry.commentaire,
            utilisateur_nom_complet=utilisateur_nom_complet,
            date_changement=entry.date_changement.isoformat(),
        )
