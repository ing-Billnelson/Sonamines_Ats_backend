"""Use case pour la validation d'un compte utilisateur."""

from ...domain.entities import Utilisateur
from ...domain.enums import StatutCompte, TypeEvenement
from ...domain.exceptions import CodeValidationInvalideError, UtilisateurIntrouvableError
from ...domain.ports import UtilisateurRepository
from ...domain.value_objects import Email
from ..dto import UtilisateurDTO, ValiderCompteDTO
from .notifier_utilisateur import NotifierUtilisateurUseCase


class ValiderCompteUseCase:
    """Use case pour valider un compte utilisateur avec un code de validation."""

    def __init__(
        self,
        utilisateur_repository: UtilisateurRepository,
        notifier_utilisateur: NotifierUtilisateurUseCase,
    ):
        self._utilisateur_repository = utilisateur_repository
        self._notifier_utilisateur = notifier_utilisateur

    async def executer(self, donnees: ValiderCompteDTO) -> UtilisateurDTO:
        """
        Valide un compte utilisateur avec un code de validation.

        Args:
            donnees: Données de validation du compte

        Returns:
            UtilisateurDTO: Informations de l'utilisateur validé

        Raises:
            UtilisateurIntrouvableError: Si l'utilisateur n'existe pas
            CodeValidationInvalideError: Si le code de validation est incorrect ou expiré
            ValueError: Si le compte est déjà validé
        """
        # Récupérer l'utilisateur par email
        email = Email(donnees.email)
        utilisateur = await self._utilisateur_repository.obtenir_par_email(email)

        if not utilisateur:
            raise UtilisateurIntrouvableError(donnees.email)

        # Vérifier que le compte n'est pas déjà validé
        if utilisateur.statut == StatutCompte.ACTIF:
            raise ValueError("Le compte est déjà validé")

        # Vérifier le code de validation fourni par l'utilisateur
        if not utilisateur.code_validation_est_valide(donnees.code_validation):
            raise CodeValidationInvalideError()

        # Valider le compte
        utilisateur.valider_compte()

        # Sauvegarder les modifications
        if hasattr(utilisateur, "photo_url"):  # Candidat
            utilisateur_sauvegarde = (
                await self._utilisateur_repository.sauvegarder_candidat(utilisateur)
            )
        else:  # Administrateur
            # Déterminer le type d'admin et sauvegarder approprié
            # TODO: Implémenter la logique de distinction admin RH/super admin
            utilisateur_sauvegarde = utilisateur

        # Envoyer la notification de validation
        await self._notifier_utilisateur.executer(
            utilisateur=utilisateur_sauvegarde,
            evenement=TypeEvenement.COMPTE_VALIDE,
            contenu="Votre compte a été validé avec succès. Vous pouvez maintenant vous connecter.",
        )

        # Convertir en DTO pour la réponse
        return self._convertir_en_dto(utilisateur_sauvegarde)

    def _convertir_en_dto(self, utilisateur: Utilisateur) -> UtilisateurDTO:
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