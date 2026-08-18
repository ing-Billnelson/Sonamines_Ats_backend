"""Use case pour l'authentification des utilisateurs."""

from datetime import datetime, timedelta
from typing import Dict, Any
from uuid import UUID

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHashError
from jose import jwt, JWTError

from ...domain.entities import (
    AdministrateurRH,
    Candidat,
    SuperAdministrateur,
    Utilisateur,
)
from ...domain.exceptions import (
    AuthentificationEchoueeError,
    UtilisateurIntrouvableError,
)
from ...domain.ports import UtilisateurRepository
from ...domain.value_objects import Email
from ..dto import AuthentificationDTO, TokenDTO, UtilisateurDTO


class AuthentifierUseCase:
    """Use case pour l'authentification des utilisateurs."""

    def __init__(
        self,
        utilisateur_repository: UtilisateurRepository,
        password_hasher: PasswordHasher,
        jwt_secret_key: str,
        jwt_algorithm: str = "HS256",
        jwt_expire_minutes: int = 30,
    ):
        self._utilisateur_repository = utilisateur_repository
        self._password_hasher = password_hasher
        self._jwt_secret_key = jwt_secret_key
        self._jwt_algorithm = jwt_algorithm
        self._jwt_expire_minutes = jwt_expire_minutes

    async def executer(self, donnees: AuthentificationDTO) -> TokenDTO:
        """
        Authentifie un utilisateur et génère un token JWT.

        Args:
            donnees: Données d'authentification (email + mot de passe)

        Returns:
            TokenDTO: Token d'accès et informations utilisateur

        Raises:
            AuthentificationEchoueeError: Si l'authentification échoue
        """
        try:
            # Récupérer l'utilisateur par email
            email = Email(donnees.email)
            utilisateur = await self._utilisateur_repository.obtenir_par_email(email)

            if not utilisateur:
                raise AuthentificationEchoueeError("Identifiants incorrects")

            # Vérifier que le compte peut se connecter
            if not utilisateur.peut_se_connecter():
                raise AuthentificationEchoueeError(
                    f"Compte {utilisateur.statut.value.lower()}, connexion impossible"
                )

            # Vérifier le mot de passe
            try:
                self._password_hasher.verify(
                    utilisateur.mot_de_passe_hash, donnees.mot_de_passe
                )
            except (VerifyMismatchError, InvalidHashError):
                raise AuthentificationEchoueeError("Identifiants incorrects")

            # Mettre à jour la date de dernière connexion
            utilisateur.date_derniere_connexion = datetime.utcnow()
            await self._sauvegarder_utilisateur(utilisateur)

            # Générer le token JWT
            token_data = self._creer_token_jwt(utilisateur)

            # Convertir l'utilisateur en DTO
            utilisateur_dto = self._convertir_en_dto(utilisateur)

            return TokenDTO(
                access_token=token_data["access_token"],
                token_type="bearer",
                expires_in=token_data["expires_in"],
                utilisateur=utilisateur_dto,
            )

        except AuthentificationEchoueeError:
            raise
        except Exception as e:
            raise AuthentificationEchoueeError(f"Erreur d'authentification: {e}")

    async def verifier_token(self, token: str) -> UtilisateurDTO:
        """
        Vérifie un token JWT et retourne l'utilisateur associé.

        Args:
            token: Token JWT à vérifier

        Returns:
            UtilisateurDTO: Informations de l'utilisateur

        Raises:
            AuthentificationEchoueeError: Si le token est invalide
        """
        try:
            # Décoder le token
            payload = jwt.decode(
                token, self._jwt_secret_key, algorithms=[self._jwt_algorithm]
            )

            # Extraire l'ID utilisateur
            user_id: str = payload.get("sub")
            if not user_id:
                raise AuthentificationEchoueeError("Token invalide")

            # Récupérer l'utilisateur
            utilisateur = await self._utilisateur_repository.obtenir_par_id(
                UUID(user_id)
            )
            if not utilisateur:
                raise AuthentificationEchoueeError("Utilisateur introuvable")

            # Vérifier que le compte est toujours actif
            if not utilisateur.peut_se_connecter():
                raise AuthentificationEchoueeError("Compte inactif")

            return self._convertir_en_dto(utilisateur)

        except JWTError:
            raise AuthentificationEchoueeError("Token invalide")
        except Exception as e:
            raise AuthentificationEchoueeError(f"Erreur de vérification: {e}")

    def _creer_token_jwt(self, utilisateur: Utilisateur) -> Dict[str, Any]:
        """Crée un token JWT pour l'utilisateur."""
        expire = datetime.utcnow() + timedelta(minutes=self._jwt_expire_minutes)

        payload = {
            "sub": str(utilisateur.id),
            "email": str(utilisateur.email),
            "nom_complet": utilisateur.nom_complet,
            "statut": utilisateur.statut.value,
            "role": self._determiner_role(utilisateur),
            "exp": expire,
            "iat": datetime.utcnow(),
        }

        token = jwt.encode(payload, self._jwt_secret_key, algorithm=self._jwt_algorithm)

        return {
            "access_token": token,
            "expires_in": self._jwt_expire_minutes * 60,  # en secondes
        }

    async def _sauvegarder_utilisateur(self, utilisateur: Utilisateur) -> None:
        """Sauvegarde un utilisateur selon son type."""
        # Déterminer le type d'utilisateur et utiliser la bonne méthode
        if hasattr(utilisateur, "photo_url"):  # Candidat
            await self._utilisateur_repository.sauvegarder_candidat(utilisateur)
        else:
            # TODO: Implémenter la distinction admin RH/super admin
            # Pour l'instant, on suppose que c'est géré dans le repository
            pass

    def _determiner_role(self, utilisateur: Utilisateur) -> str:
        """Détermine le rôle/type d'utilisateur à partir du type concret."""
        if isinstance(utilisateur, Candidat):
            return "candidat"
        elif isinstance(utilisateur, SuperAdministrateur):
            return "super_administrateur"
        elif isinstance(utilisateur, AdministrateurRH):
            return "administrateur_rh"
        return "utilisateur"

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
            role=self._determiner_role(utilisateur),
        )
