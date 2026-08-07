"""Use case pour le téléversement de documents de candidature."""

from uuid import UUID

from ...domain.entities import Document
from ...domain.enums import CategorieFichier
from ...domain.exceptions import CandidatureIntrouvableError
from ...domain.ports import CandidatureRepository, StoragePort
from ..dto import DocumentDTO, TeleverserDocumentDTO


class TeleverserDocumentUseCase:
    """Use case pour téléverser un document de candidature."""

    def __init__(
        self,
        candidature_repository: CandidatureRepository,
        storage_port: StoragePort,
    ):
        self._candidature_repository = candidature_repository
        self._storage_port = storage_port

    async def executer(self, donnees: TeleverserDocumentDTO) -> DocumentDTO:
        """
        Téléverse un document pour une candidature.

        Args:
            donnees: Données de téléversement du document

        Returns:
            DocumentDTO: Informations du document téléversé

        Raises:
            CandidatureIntrouvableError: Si la candidature n'existe pas
            FichierTropVolumineuxError: Si le document est trop volumineux
            FormatFichierNonSupporteError: Si le format n'est pas supporté
        """
        candidature_id = UUID(donnees.candidature_id)
        telechargeur_id = UUID(donnees.telechargeur_id)

        # Vérifier que la candidature existe
        candidature = await self._candidature_repository.obtenir_par_id(candidature_id)
        if not candidature:
            raise CandidatureIntrouvableError(donnees.candidature_id)

        # Téléverser le fichier
        # Le StoragePort se charge de valider la taille et le format
        url_stockage = await self._storage_port.televerser(
            fichier=donnees.contenu,
            nom_original=donnees.nom_original,
            categorie=CategorieFichier.DOCUMENT,
            proprietaire_id=telechargeur_id,
        )

        # Générer un nom de fichier unique pour le stockage
        nom_fichier_stockage = self._generer_nom_fichier_stockage(
            donnees.nom_original, telechargeur_id
        )

        # Créer l'entité document
        document = Document.creer_nouveau(
            candidature_id=candidature_id,
            type_document=donnees.type_document,
            nom_original=donnees.nom_original,
            nom_fichier_stockage=nom_fichier_stockage,
            url_stockage=url_stockage,
            taille_octets=len(donnees.contenu),
            type_mime=donnees.type_mime,
            telechargeur_id=telechargeur_id,
        )

        # Sauvegarder le document
        document_sauvegarde = await self._candidature_repository.sauvegarder_document(
            document
        )

        # TODO: Vérifier si la candidature est maintenant complète et notifier
        # await self._verifier_completude_candidature(candidature)

        return await self._convertir_en_dto(document_sauvegarde)

    def _generer_nom_fichier_stockage(self, nom_original: str, telechargeur_id: UUID) -> str:
        """Génère un nom de fichier unique pour le stockage."""
        import time
        from pathlib import Path

        extension = Path(nom_original).suffix
        timestamp = int(time.time() * 1000)  # timestamp en millisecondes
        return f"{telechargeur_id}_{timestamp}{extension}"

    async def _convertir_en_dto(self, document: Document) -> DocumentDTO:
        """Convertit un document en DTO."""
        # Générer une URL temporaire d'accès au document
        url_temporaire = await self._storage_port.generer_url_temporaire(
            document.url_stockage
        )

        # TODO: Récupérer le nom complet du téléchargeur
        telechargeur_nom_complet = "Utilisateur"  # Placeholder

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