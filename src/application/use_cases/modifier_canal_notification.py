"""Use case pour la modification du canal de notification."""

from uuid import UUID

from ...domain.enums import CanalNotification, TypeEvenement
from ...domain.exceptions import (
    UtilisateurIntrouvableError,
    CanalNonVerifieError,
)
from ...domain.ports import UtilisateurRepository
from ..dto import ModifierCanalNotificationDTO, UtilisateurDTO
from .notifier_utilisateur import NotifierUtilisateurUseCase


class ModifierCanalNotificationUseCase:
    """Use case pour modifier le canal de notification d'un utilisateur."""

    def __init__(
        self,
        utilisateur_repository: UtilisateurRepository,
        notifier_utilisateur: NotifierUtilisateurUseCase,
    ):
        self._utilisateur_repository = utilisateur_repository
        self._notifier_utilisateur = notifier_utilisateur

    async def executer(self, donnees: ModifierCanalNotificationDTO) -> UtilisateurDTO:
        """
        Modifie le canal de notification d'un utilisateur.

        Args:
            donnees: Données de modification du canal

        Returns:
            UtilisateurDTO: Informations de l'utilisateur mis à jour

        Raises:
            UtilisateurIntrouvableError: Si l'utilisateur n'existe pas
            CanalNonVerifieError: Si le nouveau canal n'est pas vérifié
            ValueError: Si le canal demandé n'est pas valide
        """
        # Récupérer l'utilisateur
        utilisateur_id = UUID(donnees.utilisateur_id)
        utilisateur = await self._utilisateur_repository.obtenir_par_id(utilisateur_id)

        if not utilisateur:
            raise UtilisateurIntrouvableError(donnees.utilisateur_id)

        # Vérifier si le changement est nécessaire
        if utilisateur.canal_validation == donnees.nouveau_canal:
            # Pas de changement nécessaire, retourner l'utilisateur actuel
            return self._convertir_en_dto(utilisateur)

        # Valider que le nouveau canal peut être utilisé
        self._valider_nouveau_canal(utilisateur, donnees.nouveau_canal)

        # Sauvegarder l'ancien canal pour la notification
        ancien_canal = utilisateur.canal_validation

        # Modifier le canal
        try:
            utilisateur.changer_canal_validation(donnees.nouveau_canal)
        except ValueError as e:
            raise CanalNonVerifieError(
                donnees.nouveau_canal.value, str(e)
            )

        # Sauvegarder les modifications
        utilisateur_sauvegarde = await self._sauvegarder_utilisateur(utilisateur)

        # Notifier le changement via le NOUVEAU canal
        # (conformément à la règle : le changement prend effet immédiatement)
        await self._notifier_utilisateur.executer(
            utilisateur=utilisateur_sauvegarde,
            evenement=TypeEvenement.COMPTE_VALIDE,  # Réutiliser cet événement
            contenu=(
                f"Votre canal de notification a été modifié "
                f"de {ancien_canal.value} vers {donnees.nouveau_canal.value}."
            ),
        )

        return self._convertir_en_dto(utilisateur_sauvegarde)

    def _valider_nouveau_canal(
        self, utilisateur, nouveau_canal: CanalNotification
    ) -> None:
        """Valide que le nouveau canal peut être utilisé."""
        if nouveau_canal == CanalNotification.EMAIL:
            if not utilisateur.email or not utilisateur.email_verifie:
                raise CanalNonVerifieError(
                    nouveau_canal.value,
                    "L'email doit être défini et vérifié pour utiliser ce canal"
                )

        elif nouveau_canal == CanalNotification.SMS:
            if not utilisateur.telephone or not utilisateur.telephone_verifie:
                raise CanalNonVerifieError(
                    nouveau_canal.value,
                    "Le téléphone doit être défini et vérifié pour utiliser ce canal"
                )

        # Le canal INTERNE est toujours autorisé

    async def _sauvegarder_utilisateur(self, utilisateur) -> any:
        """Sauvegarde un utilisateur selon son type."""
        if hasattr(utilisateur, "photo_url"):  # Candidat
            return await self._utilisateur_repository.sauvegarder_candidat(utilisateur)
        else:
            # TODO: Implémenter la distinction admin RH/super admin
            # Pour l'instant, on retourne l'utilisateur tel quel
            return utilisateur

    def _convertir_en_dto(self, utilisateur) -> UtilisateurDTO:
        """Convertit un utilisateur en DTO."""
        photo_url = getattr(utilisateur, "photo_url", None)

        return UtilisateurDTO(
            id=str(utilisateur.id),
            email=str(utilisateur.email),
            telephone=str(utilisateur.telephone) if utilisateur.telephone else None,
            nom=utilisateur.nom,
            prenom=utilisateur.prenom,
            nom_complet=utilisateur.nom_complet,
            statut=utilisateur.statut,
            canal_validation=utilisateur.canal_validation,
            email_verifie=utilisateur.email_verifie,
            telephone_verifie=utilisateur.telephone_verifie,
            date_creation=utilisateur.date_creation.isoformat(),
            date_derniere_connexion=(
                utilisateur.date_derniere_connexion.isoformat()
                if utilisateur.date_derniere_connexion
                else None
            ),
            photo_url=photo_url,
        )