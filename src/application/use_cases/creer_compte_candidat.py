"""Use case pour la création d'un compte candidat."""

import uuid
from argon2 import PasswordHasher
from argon2.exceptions import HashingError

from ...domain.entities import Candidat
from ...domain.enums import TypeEvenement
from ...domain.exceptions import UtilisateurExistantError
from ...domain.ports import NotificationPort, UtilisateurRepository
from ...domain.value_objects import Email, NumeroTelephone
from ..dto import CreerCompteDTO, UtilisateurDTO
from .notifier_utilisateur import NotifierUtilisateurUseCase


class CreerCompteCandidatUseCase:
    """Use case pour créer un nouveau compte candidat."""

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
        Crée un nouveau compte candidat.

        Args:
            donnees: Données de création du compte

        Returns:
            UtilisateurDTO: Informations du candidat créé

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

        # Créer le candidat
        candidat = Candidat.creer_nouveau(
            email=email,
            telephone=telephone,
            mot_de_passe_hash=mot_de_passe_hash,
            nom=donnees.nom,
            prenom=donnees.prenom,
            canal_validation=donnees.canal_validation,
        )

        # Sauvegarder le candidat
        candidat_sauvegarde = await self._utilisateur_repository.sauvegarder_candidat(
            candidat
        )

        # Envoyer la notification de création de compte
        await self._notifier_utilisateur.executer(
            utilisateur=candidat_sauvegarde,
            evenement=TypeEvenement.COMPTE_CREE,
            contenu=(
                f"Votre compte candidat a été créé avec succès. Votre code de "
                f"validation est {candidat_sauvegarde.code_validation}. Ce code "
                "expire dans 5 minutes."
            ),
        )

        # Convertir en DTO pour la réponse
        return self._convertir_en_dto(candidat_sauvegarde)

    def _convertir_en_dto(self, candidat: Candidat) -> UtilisateurDTO:
        """Convertit un candidat en DTO utilisateur."""
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