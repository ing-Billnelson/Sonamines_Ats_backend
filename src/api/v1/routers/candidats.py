"""Router pour les opérations des candidats."""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from typing import List

from ....application.use_cases import (
    SoumettreCandidatureSpontaneeUseCase,
    PostulerOffreUseCase,
    TeleverserDocumentUseCase,
)
from ....application.dto import (
    SoumettreKandidatureDTO,
    TeleverserDocumentDTO,
)
from ....domain.entities.document import TypeDocument
from ....domain.exceptions import (
    UtilisateurIntrouvableError,
    OffreClotureeError,
    CandidatureNonEligibleError,
)
from ..schemas import (
    SoumettreKandidatureRequest,
    CandidatureResponse,
    TeleverserDocumentRequest,
    DocumentResponse,
)
from ..dependencies import (
    get_utilisateur_courant,
    get_soumettre_candidature_spontanee_use_case,
    get_televerser_document_use_case,
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
    # use_case: PostulerOffreUseCase = Depends(get_postuler_offre_use_case),
):
    """Postule à une offre spécifique."""
    # TODO: Implémenter avec le use case réel
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail={"error": "NotImplemented", "message": "Endpoint en cours d'implémentation"},
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