"""Use case pour le téléversement de photo de profil."""

from uuid import UUID

from ...domain.enums import CategorieFichier
from ...domain.exceptions import (
    UtilisateurIntrouvableError,
    AutorisationRefuseeError,
)
from ...domain.ports import StoragePort, UtilisateurRepository
from ..dto import UtilisateurDTO


class TeleverserPhotoProfilUseCase:
    """Use case pour téléverser une photo de profil de candidat."""

    def __init__(
        self,
        utilisateur_repository: UtilisateurRepository,
        storage_port: StoragePort,
    ):
        self._utilisateur_repository = utilisateur_repository
        self._storage_port = storage_port

    async def executer(
        self,
        candidat_id: str,
        fichier: bytes,
        nom_original: str,
    ) -> UtilisateurDTO:
        """
        Téléverse une photo de profil pour un candidat.

        Args:
            candidat_id: ID du candidat (UUID en string)
            fichier: Contenu binaire de la photo
            nom_original: Nom original du fichier

        Returns:
            UtilisateurDTO: Informations du candidat mis à jour

        Raises:
            UtilisateurIntrouvableError: Si le candidat n'existe pas
            AutorisationRefuseeError: Si l'utilisateur n'est pas un candidat
            FichierTropVolumineuxError: Si la photo est trop volumineuse
            FormatFichierNonSupporteError: Si le format n'est pas supporté
        """
        # Récupérer le candidat
        candidat_uuid = UUID(candidat_id)
        candidat = await self._utilisateur_repository.obtenir_candidat_par_id(
            candidat_uuid
        )

        if not candidat:
            raise UtilisateurIntrouvableError(candidat_id)

        # Vérifier que c'est bien un candidat (a l'attribut photo_url)
        if not hasattr(candidat, "photo_url"):
            raise AutorisationRefuseeError(
                "Seuls les candidats peuvent avoir une photo de profil"
            )

        # Supprimer l'ancienne photo si elle existe
        if candidat.photo_url:
            await self._storage_port.supprimer(
                candidat.photo_url, CategorieFichier.PHOTO
            )

        # Téléverser la nouvelle photo
        # Le StoragePort se charge de valider la taille et le format
        nouvelle_url = await self._storage_port.televerser(
            fichier=fichier,
            nom_original=nom_original,
            categorie=CategorieFichier.PHOTO,
            proprietaire_id=candidat.id,
        )

        # Mettre à jour le candidat
        candidat.definir_photo_profil(nouvelle_url)

        # Sauvegarder les modifications
        candidat_sauvegarde = await self._utilisateur_repository.sauvegarder_candidat(
            candidat
        )

        return self._convertir_en_dto(candidat_sauvegarde)

    def _convertir_en_dto(self, candidat) -> UtilisateurDTO:
        """Convertit un candidat en DTO."""
        return UtilisateurDTO(
            id=str(candidat.id),
            email=str(candidat.email),
            telephone=str(candidat.telephone) if candidat.telephone else None,
            nom=candidat.nom,
            prenom=candidat.prenom,
            nom_complet=candidat.nom_complet,
            statut=candidat.statut,
            canal_validation=candidat.canal_validation,
            email_verifie=candidat.email_verifie,
            telephone_verifie=candidat.telephone_verifie,
            date_creation=candidat.date_creation.isoformat(),
            date_derniere_connexion=(
                candidat.date_derniere_connexion.isoformat()
                if candidat.date_derniere_connexion
                else None
            ),
            photo_url=candidat.photo_url,
        )