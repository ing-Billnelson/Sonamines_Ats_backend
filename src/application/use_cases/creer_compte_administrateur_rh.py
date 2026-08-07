"""Use case pour la création d'un compte administrateur RH."""

from argon2 import PasswordHasher
from argon2.exceptions import HashingError

from ...domain.entities import AdministrateurRH
from ...domain.enums import TypeEvenement
from ...domain.exceptions import UtilisateurExistantError
from ...domain.ports import UtilisateurRepository
from ...domain.value_objects import Email, NumeroTelephone
from ..dto import CreerCompteDTO, UtilisateurDTO
from .notifier_utilisateur import NotifierUtilisateurUseCase


class CreerCompteAdministrateurRHUseCase:
    """Use case pour créer un nouveau compte administrateur RH."""

    def __init__(
        self,
        utilisateur_repository: UtilisateurRepository,
        notifier_utilisateur: NotifierUtilisateurUseCase,
        password_hasher: PasswordHasher,
    ):
        self._utilisateur_repository = utilisateur_repository
        self._notifier_utilisateur = notifier_utilisateur
        self._password_hasher = password_hasher

    async def executer(self, donnees: CreerCompteDTO) -> UtilisateurDTO:
        """
        Crée un nouveau compte administrateur RH.

        Args:
            donnees: Données de création du compte

        Returns:
            UtilisateurDTO: Informations de l'administrateur créé

        Raises:
            UtilisateurExistantError: Si l'email existe déjà
            ValueError: Si les données sont invalides
            HashingError: Si le hachage du mot de passe échoue
        """
        # Validation des données d'entrée
        email = Email(donnees.email)
        telephone = (
            NumeroTelephone(donnees.telephone) if donnees.telephone else None
        )

        # Vérifier que l'email n'existe pas déjà
        if await self._utilisateur_repository.email_existe(email):
            raise UtilisateurExistantError(donnees.email)

        # Hacher le mot de passe
        try:
            mot_de_passe_hash = self._password_hasher.hash(donnees.mot_de_passe)
        except HashingError as e:
            raise ValueError(f"Erreur lors du hachage du mot de passe: {e}")

        # Créer l'administrateur RH
        admin_rh = AdministrateurRH.creer_nouveau(
            email=email,
            telephone=telephone,
            mot_de_passe_hash=mot_de_passe_hash,
            nom=donnees.nom,
            prenom=donnees.prenom,
            canal_validation=donnees.canal_validation,
        )

        # Sauvegarder l'administrateur
        admin_sauvegarde = await self._utilisateur_repository.sauvegarder_admin_rh(
            admin_rh
        )

        # Envoyer la notification de création de compte
        await self._notifier_utilisateur.executer(
            utilisateur=admin_sauvegarde,
            evenement=TypeEvenement.COMPTE_CREE,
            contenu=f"Votre compte administrateur RH a été créé avec succès. "
            f"Un code de validation a été envoyé via {donnees.canal_validation.value}.",
        )

        # Convertir en DTO pour la réponse
        return self._convertir_en_dto(admin_sauvegarde)

    def _convertir_en_dto(self, admin: AdministrateurRH) -> UtilisateurDTO:
        """Convertit un administrateur RH en DTO utilisateur."""
        return UtilisateurDTO(
            id=str(admin.id),
            email=str(admin.email),
            telephone=str(admin.telephone) if admin.telephone else None,
            nom=admin.nom,
            prenom=admin.prenom,
            nom_complet=admin.nom_complet,
            statut=admin.statut,
            canal_validation=admin.canal_validation,
            email_verifie=admin.email_verifie,
            telephone_verifie=admin.telephone_verifie,
            date_creation=admin.date_creation.isoformat(),
            date_derniere_connexion=(
                admin.date_derniere_connexion.isoformat()
                if admin.date_derniere_connexion
                else None
            ),
            photo_url=None,  # Les admins n'ont pas de photo
        )