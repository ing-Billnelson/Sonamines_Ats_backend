"""Use case pour la suppression de photo de profil."""

from uuid import UUID

from ...domain.enums import CategorieFichier
from ...domain.exceptions import (
    UtilisateurIntrouvableError,
    AutorisationRefuseeError,
)
from ...domain.ports import StoragePort, UtilisateurRepository
from ..dto import UtilisateurDTO


class SupprimerPhotoProfilUseCase:
    """Use case pour supprimer la photo de profil d'un candidat."""

    def __init__(
        self,
        utilisateur_repository: UtilisateurRepository,
        storage_port: StoragePort,
    ):
        self._utilisateur_repository = utilisateur_repository
        self._storage_port = storage_port

    async def executer(self, candidat_id: str) -> UtilisateurDTO:
        """
        Supprime la photo de profil d'un candidat.

        Args:
            candidat_id: ID du candidat (UUID en string)

        Returns:
            UtilisateurDTO: Informations du candidat mis à jour

        Raises:
            UtilisateurIntrouvableError: Si le candidat n'existe pas
            AutorisationRefuseeError: Si l'utilisateur n'est pas un candidat
            ValueError: Si le candidat n'a pas de photo de profil
        """
        # Récupérer le candidat
        candidat_uuid = UUID(candidat_id)
        candidat = await self._utilisateur_repository.obtenir_candidat_par_id(
            candidat_uuid
        )

        if not candidat:
            raise UtilisateurIntrouvableError(candidat_id)

        # Vérifier que c'est bien un candidat
        if not hasattr(candidat, "photo_url"):
            raise AutorisationRefuseeError(
                "Seuls les candidats peuvent avoir une photo de profil"
            )

        # Vérifier qu'il y a une photo à supprimer
        if not candidat.a_photo_profil():
            raise ValueError("Le candidat n'a pas de photo de profil à supprimer")

        # Supprimer la photo du stockage
        ancienne_url = candidat.photo_url
        await self._storage_port.supprimer(ancienne_url, CategorieFichier.PHOTO)

        # Mettre à jour le candidat
        candidat.supprimer_photo_profil()

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