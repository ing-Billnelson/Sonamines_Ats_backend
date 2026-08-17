"""Router pour les opérations des candidats."""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from typing import List, Optional
from uuid import UUID

from ....application.use_cases import (
    SoumettreCandidatureSpontaneeUseCase,
    PostulerOffreUseCase,
    TeleverserDocumentUseCase,
    TeleverserPhotoProfilUseCase,
    SupprimerPhotoProfilUseCase,
)
from ....application.dto import (
    SoumettreKandidatureDTO,
    TeleverserDocumentDTO,
    UtilisateurDTO,
)
from ....domain.entities.document import TypeDocument
from ....domain.enums import CategorieFichier
from ....domain.exceptions import (
    UtilisateurIntrouvableError,
    OffreClotureeError,
    OffreIntrouvableError,
    CandidatureDejaExistanteError,
    CandidatureNonEligibleError,
    StockageIndisponibleError,
)
from ....domain.ports import CandidatureRepository, StoragePort
from ..schemas import (
    SoumettreKandidatureRequest,
    CandidatureResponse,
    TeleverserDocumentRequest,
    DocumentResponse,
    UtilisateurResponse,
    SuccessResponse,
)
from ..dependencies import (
    get_utilisateur_courant,
    get_soumettre_candidature_spontanee_use_case,
    get_postuler_offre_use_case,
    get_televerser_document_use_case,
    get_televerser_photo_profil_use_case,
    get_supprimer_photo_profil_use_case,
    get_candidature_repository,
    get_storage_adapter,
)

router = APIRouter(prefix="/candidats", tags=["Candidats"])


@router.post(
    "/candidatures/spontanees",
    response_model=CandidatureResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Soumettre une candidature spontanée",
    description="Soumet une candidature spontanée (sans offre spécifique)",
)
async def soumettre_candidature_spontanee(
    donnees: SoumettreKandidatureRequest,
    utilisateur_courant = Depends(get_utilisateur_courant),
    use_case: SoumettreCandidatureSpontaneeUseCase = Depends(get_soumettre_candidature_spontanee_use_case),
):
    """Soumet une candidature spontanée."""
    try:
        # Vérifier que c'est bien une candidature spontanée
        if donnees.offre_id is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "ValidationError",
                    "message": "Une candidature spontanée ne doit pas avoir d'offre associée"
                },
            )

        # Convertir en DTO
        dto = SoumettreKandidatureDTO(
            candidat_id=utilisateur_courant.id,
            message_motivation=donnees.message_motivation,
            offre_id=None,  # Candidature spontanée
        )

        # Exécuter le use case
        candidature_dto = await use_case.executer(dto)

        # TODO: Convertir le DTO en schema de réponse
        # Pour l'instant, retourner un placeholder
        return CandidatureResponse(
            id=candidature_dto.id,
            numero_reference=candidature_dto.numero_reference,
            candidat_nom_complet=candidature_dto.candidat_nom_complet,
            candidat_email=candidature_dto.candidat_email,
            offre_titre=None,
            offre_numero_reference=None,
            statut=candidature_dto.statut,
            message_motivation=candidature_dto.message_motivation,
            notes_internes=candidature_dto.notes_internes,
            date_soumission=candidature_dto.date_soumission,
            date_derniere_modification=candidature_dto.date_derniere_modification,
            documents=[],
            historique=[],
            est_spontanee=True,
            est_complete=candidature_dto.est_complete,
        )

    except UtilisateurIntrouvableError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "UtilisateurIntrouvable", "message": str(e)},
        )


@router.post(
    "/candidatures/offres/{offre_id}",
    response_model=CandidatureResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Postuler à une offre",
    description="Soumet une candidature pour une offre spécifique",
)
async def postuler_offre(
    offre_id: str,
    donnees: SoumettreKandidatureRequest,
    utilisateur_courant = Depends(get_utilisateur_courant),
    use_case: PostulerOffreUseCase = Depends(get_postuler_offre_use_case),
):
    """Postule à une offre spécifique."""
    try:
        dto = SoumettreKandidatureDTO(
            candidat_id=utilisateur_courant.id,
            message_motivation=donnees.message_motivation,
            offre_id=offre_id,
        )

        candidature_dto = await use_case.executer(dto)

        return CandidatureResponse(
            id=candidature_dto.id,
            numero_reference=candidature_dto.numero_reference,
            candidat_nom_complet=candidature_dto.candidat_nom_complet,
            candidat_email=candidature_dto.candidat_email,
            offre_titre=candidature_dto.offre_titre,
            offre_numero_reference=candidature_dto.offre_numero_reference,
            statut=candidature_dto.statut,
            message_motivation=candidature_dto.message_motivation,
            notes_internes=candidature_dto.notes_internes,
            date_soumission=candidature_dto.date_soumission,
            date_derniere_modification=candidature_dto.date_derniere_modification,
            documents=candidature_dto.documents,
            historique=candidature_dto.historique,
            est_spontanee=candidature_dto.est_spontanee,
            est_complete=candidature_dto.est_complete,
        )

    except OffreIntrouvableError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "OffreIntrouvable", "message": str(e)},
        )
    except UtilisateurIntrouvableError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "UtilisateurIntrouvable", "message": str(e)},
        )
    except OffreClotureeError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error": "OffreIndisponible", "message": str(e)},
        )
    except CandidatureDejaExistanteError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error": "CandidatureDejaExistante", "message": str(e)},
        )


@router.get(
    "/candidatures",
    response_model=List[CandidatureResponse],
    summary="Lister mes candidatures",
    description="Liste toutes les candidatures du candidat connecté",
)
async def lister_mes_candidatures(
    utilisateur_courant = Depends(get_utilisateur_courant),
):
    """Liste les candidatures du candidat connecté."""
    # TODO: Implémenter le listage des candidatures
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail={"error": "NotImplemented", "message": "Endpoint en cours d'implémentation"},
    )


@router.post(
    "/candidatures/{candidature_id}/documents",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Téléverser un document",
    description="Téléverse un document pour une candidature",
)
async def televerser_document(
    candidature_id: str,
    type_document: TypeDocument = Form(..., description="Type de document"),
    fichier: UploadFile = File(..., description="Fichier à téléverser"),
    utilisateur_courant = Depends(get_utilisateur_courant),
    use_case: TeleverserDocumentUseCase = Depends(get_televerser_document_use_case),
):
    """Téléverse un document pour une candidature."""
    try:
        # Lire le contenu du fichier
        contenu_fichier = await fichier.read()

        # Convertir en DTO
        dto = TeleverserDocumentDTO(
            candidature_id=candidature_id,
            type_document=type_document,
            nom_original=fichier.filename or "document",
            contenu=contenu_fichier,
            type_mime=fichier.content_type or "application/octet-stream",
            telechargeur_id=utilisateur_courant.id,
        )

        # Exécuter le use case
        document_dto = await use_case.executer(dto)

        return DocumentResponse(
            id=document_dto.id,
            type_document=document_dto.type_document,
            nom_original=document_dto.nom_original,
            taille_octets=document_dto.taille_octets,
            type_mime=document_dto.type_mime,
            url_temporaire=document_dto.url_temporaire,
            date_telechargement=document_dto.date_telechargement,
            telechargeur_nom_complet=document_dto.telechargeur_nom_complet,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error": "ValidationError", "message": str(e)},
        )


@router.post(
    "/photo-profil",
    response_model=UtilisateurResponse,
    status_code=status.HTTP_200_OK,
    summary="Téléverser une photo de profil",
    description="Téléverse la photo de profil du candidat connecté",
)
async def televerser_photo_profil_candidat(
    photo: UploadFile = File(..., description="Fichier image (JPG, JPEG, PNG)"),
    utilisateur_courant: UtilisateurDTO = Depends(get_utilisateur_courant),
    use_case: TeleverserPhotoProfilUseCase = Depends(get_televerser_photo_profil_use_case),
):
    """Téléverse la photo de profil du candidat connecté."""
    contenu_fichier = await photo.read()

    utilisateur_dto = await use_case.executer(
        candidat_id=utilisateur_courant.id,
        fichier=contenu_fichier,
        nom_original=photo.filename or "photo_profil",
    )

    return _convertir_utilisateur_dto(utilisateur_dto)


@router.delete(
    "/photo-profil",
    response_model=UtilisateurResponse,
    summary="Supprimer la photo de profil",
    description="Supprime la photo de profil du candidat connecté",
)
async def supprimer_photo_profil_candidat(
    utilisateur_courant: UtilisateurDTO = Depends(get_utilisateur_courant),
    use_case: SupprimerPhotoProfilUseCase = Depends(get_supprimer_photo_profil_use_case),
):
    """Supprime la photo de profil du candidat connecté."""
    utilisateur_dto = await use_case.executer(candidat_id=utilisateur_courant.id)

    return _convertir_utilisateur_dto(utilisateur_dto)


@router.get(
    "/candidatures/{candidature_id}/documents",
    response_model=List[DocumentResponse],
    summary="Lister les documents d'une candidature",
    description="Liste les documents d'une candidature avec des URLs présignées",
)
async def lister_documents_candidature(
    candidature_id: str,
    utilisateur_courant: UtilisateurDTO = Depends(get_utilisateur_courant),
    candidature_repository: CandidatureRepository = Depends(get_candidature_repository),
    storage_port: StoragePort = Depends(get_storage_adapter),
):
    """Liste les documents d'une candidature avec des URLs présignées."""
    candidature = await candidature_repository.obtenir_par_id(UUID(candidature_id))
    if not candidature:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "CandidatureIntrouvable", "message": f"Candidature introuvable: {candidature_id}"},
        )

    if candidature.candidat_id != UUID(utilisateur_courant.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": "AutorisationRefusee", "message": "Vous n'êtes pas autorisé à consulter cette candidature"},
        )

    documents = await candidature_repository.obtenir_documents_candidature(
        UUID(candidature_id)
    )

    reponses = []
    for document in documents:
        url_temporaire = await storage_port.generer_url_temporaire(
            document.url_stockage
        )
        reponses.append(
            DocumentResponse(
                id=str(document.id),
                type_document=document.type_document,
                nom_original=document.nom_original,
                taille_octets=document.taille_octets,
                type_mime=document.type_mime,
                url_temporaire=url_temporaire,
                date_telechargement=document.date_telechargement.isoformat(),
                telechargeur_nom_complet="",
            )
        )

    return reponses


@router.delete(
    "/candidatures/{candidature_id}/documents/{document_id}",
    response_model=SuccessResponse,
    summary="Supprimer un document d'une candidature",
    description="Supprime un document d'une candidature (stockage + référence)",
)
async def supprimer_document_candidature(
    candidature_id: str,
    document_id: str,
    utilisateur_courant: UtilisateurDTO = Depends(get_utilisateur_courant),
    candidature_repository: CandidatureRepository = Depends(get_candidature_repository),
    storage_port: StoragePort = Depends(get_storage_adapter),
):
    """Supprime un document d'une candidature."""
    candidature = await candidature_repository.obtenir_par_id(UUID(candidature_id))
    if not candidature:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "CandidatureIntrouvable", "message": f"Candidature introuvable: {candidature_id}"},
        )

    if candidature.candidat_id != UUID(utilisateur_courant.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": "AutorisationRefusee", "message": "Vous n'êtes pas autorisé à modifier cette candidature"},
        )

    documents = await candidature_repository.obtenir_documents_candidature(
        UUID(candidature_id)
    )
    document_cible = next(
        (doc for doc in documents if doc.id == UUID(document_id)), None
    )
    if not document_cible:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "DocumentIntrouvable", "message": f"Document introuvable: {document_id}"},
        )

    try:
        supprime = await storage_port.supprimer(
            document_cible.url_stockage, CategorieFichier.DOCUMENT
        )
    except Exception as e:
        raise StockageIndisponibleError(
            f"Le service de stockage est momentanément indisponible: {e}"
        )
    if not supprime:
        raise StockageIndisponibleError(
            "Impossible de supprimer le fichier du stockage"
        )

    await candidature_repository.supprimer_document(UUID(document_id))

    return SuccessResponse(
        success=True,
        message="Document supprimé avec succès",
    )


def _convertir_utilisateur_dto(dto: UtilisateurDTO) -> UtilisateurResponse:
    """Convertit un UtilisateurDTO en UtilisateurResponse."""
    return UtilisateurResponse(
        id=dto.id,
        email=dto.email,
        telephone=dto.telephone,
        nom=dto.nom,
        prenom=dto.prenom,
        nom_complet=dto.nom_complet,
        statut=dto.statut,
        canal_validation=dto.canal_validation,
        email_verifie=dto.email_verifie,
        telephone_verifie=dto.telephone_verifie,
        date_creation=dto.date_creation,
        date_derniere_connexion=dto.date_derniere_connexion,
        photo_url=dto.photo_url,
    )