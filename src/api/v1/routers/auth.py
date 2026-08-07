"""Router pour l'authentification."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from ....application.use_cases import (
    CreerCompteCandidatUseCase,
    ValiderCompteUseCase,
    AuthentifierUseCase,
)
from ....application.dto import (
    CreerCompteDTO,
    ValiderCompteDTO,
    AuthentificationDTO,
)
from ....domain.exceptions import (
    UtilisateurExistantError,
    AuthentificationEchoueeError,
    UtilisateurIntrouvableError,
)
from ..schemas import (
    CreerCompteRequest,
    ValiderCompteRequest,
    ConnexionRequest,
    TokenResponse,
    UtilisateurResponse,
    SuccessResponse,
)
from ..dependencies import get_creer_compte_candidat_use_case, get_authentifier_use_case

router = APIRouter(prefix="/auth", tags=["Authentification"])
security = HTTPBearer()


@router.post(
    "/candidats/inscrire",
    response_model=UtilisateurResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Créer un compte candidat",
    description="Crée un nouveau compte candidat et envoie un code de validation",
)
async def creer_compte_candidat(
    donnees: CreerCompteRequest,
    use_case: CreerCompteCandidatUseCase = Depends(get_creer_compte_candidat_use_case),
):
    """Crée un nouveau compte candidat."""
    try:
        # Convertir le schema en DTO
        dto = CreerCompteDTO(
            email=donnees.email,
            telephone=donnees.telephone,
            mot_de_passe=donnees.mot_de_passe,
            nom=donnees.nom,
            prenom=donnees.prenom,
            canal_validation=donnees.canal_validation,
        )

        # Exécuter le use case
        utilisateur_dto = await use_case.executer(dto)

        # Convertir en schema de réponse
        return UtilisateurResponse(
            id=utilisateur_dto.id,
            email=utilisateur_dto.email,
            telephone=utilisateur_dto.telephone,
            nom=utilisateur_dto.nom,
            prenom=utilisateur_dto.prenom,
            nom_complet=utilisateur_dto.nom_complet,
            statut=utilisateur_dto.statut,
            canal_validation=utilisateur_dto.canal_validation,
            email_verifie=utilisateur_dto.email_verifie,
            telephone_verifie=utilisateur_dto.telephone_verifie,
            date_creation=utilisateur_dto.date_creation,
            date_derniere_connexion=utilisateur_dto.date_derniere_connexion,
            photo_url=utilisateur_dto.photo_url,
        )

    except UtilisateurExistantError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error": "UtilisateurExistant", "message": str(e)},
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error": "ValidationError", "message": str(e)},
        )


@router.post(
    "/valider",
    response_model=UtilisateurResponse,
    summary="Valider un compte",
    description="Valide un compte utilisateur avec le code de validation reçu",
)
async def valider_compte(
    donnees: ValiderCompteRequest,
    # use_case: ValiderCompteUseCase = Depends(get_valider_compte_use_case),
):
    """Valide un compte utilisateur."""
    # TODO: Implémenter avec le use case réel
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail={"error": "NotImplemented", "message": "Endpoint en cours d'implémentation"},
    )


@router.post(
    "/connexion",
    response_model=TokenResponse,
    summary="Se connecter",
    description="Authentifie un utilisateur et retourne un token JWT",
)
async def se_connecter(
    donnees: ConnexionRequest,
    use_case: AuthentifierUseCase = Depends(get_authentifier_use_case),
):
    """Authentifie un utilisateur."""
    try:
        # Convertir le schema en DTO
        dto = AuthentificationDTO(
            email=donnees.email,
            mot_de_passe=donnees.mot_de_passe,
        )

        # Exécuter le use case
        token_dto = await use_case.executer(dto)

        # Convertir en schema de réponse
        return TokenResponse(
            access_token=token_dto.access_token,
            token_type=token_dto.token_type,
            expires_in=token_dto.expires_in,
            utilisateur=UtilisateurResponse(
                id=token_dto.utilisateur.id,
                email=token_dto.utilisateur.email,
                telephone=token_dto.utilisateur.telephone,
                nom=token_dto.utilisateur.nom,
                prenom=token_dto.utilisateur.prenom,
                nom_complet=token_dto.utilisateur.nom_complet,
                statut=token_dto.utilisateur.statut,
                canal_validation=token_dto.utilisateur.canal_validation,
                email_verifie=token_dto.utilisateur.email_verifie,
                telephone_verifie=token_dto.utilisateur.telephone_verifie,
                date_creation=token_dto.utilisateur.date_creation,
                date_derniere_connexion=token_dto.utilisateur.date_derniere_connexion,
                photo_url=token_dto.utilisateur.photo_url,
            ),
        )

    except AuthentificationEchoueeError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "AuthentificationEchouee", "message": str(e)},
        )


@router.get(
    "/moi",
    response_model=UtilisateurResponse,
    summary="Profil utilisateur",
    description="Récupère le profil de l'utilisateur connecté",
)
async def obtenir_profil(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    use_case: AuthentifierUseCase = Depends(get_authentifier_use_case),
):
    """Récupère le profil de l'utilisateur connecté."""
    try:
        # Vérifier le token
        utilisateur_dto = await use_case.verifier_token(credentials.credentials)

        return UtilisateurResponse(
            id=utilisateur_dto.id,
            email=utilisateur_dto.email,
            telephone=utilisateur_dto.telephone,
            nom=utilisateur_dto.nom,
            prenom=utilisateur_dto.prenom,
            nom_complet=utilisateur_dto.nom_complet,
            statut=utilisateur_dto.statut,
            canal_validation=utilisateur_dto.canal_validation,
            email_verifie=utilisateur_dto.email_verifie,
            telephone_verifie=utilisateur_dto.telephone_verifie,
            date_creation=utilisateur_dto.date_creation,
            date_derniere_connexion=utilisateur_dto.date_derniere_connexion,
            photo_url=utilisateur_dto.photo_url,
        )

    except AuthentificationEchoueeError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "TokenInvalide", "message": str(e)},
        )