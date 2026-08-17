"""Tests unitaires du use case TeleverserDocumentUseCase."""

from datetime import datetime
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.application.dto import TeleverserDocumentDTO
from src.application.use_cases.televerser_document import TeleverserDocumentUseCase
from src.domain.entities import Candidature
from src.domain.entities.document import TypeDocument
from src.domain.enums import CategorieFichier, StatutCandidature
from src.domain.exceptions import (
    AutorisationRefuseeError,
    CandidatureIntrouvableError,
)
from src.domain.value_objects import NumeroReference


def _candidature(candidat_id):
    """Construit une entité candidature."""
    return Candidature(
        id=uuid4(),
        numero_reference=NumeroReference.generer_candidature(),
        candidat_id=candidat_id,
        offre_id=None,
        statut=StatutCandidature.RECUE,
        message_motivation="Motivation valide pour la candidature de test.",
        date_soumission=datetime.utcnow(),
        date_derniere_modification=datetime.utcnow(),
    )


def _build_use_case(candidature_repository, storage_port) -> TeleverserDocumentUseCase:
    """Construit le use case avec des ports injectés."""
    return TeleverserDocumentUseCase(
        candidature_repository=candidature_repository,
        storage_port=storage_port,
    )


def _donnees(candidature_id, telechargeur_id) -> TeleverserDocumentDTO:
    return TeleverserDocumentDTO(
        candidature_id=str(candidature_id),
        type_document=TypeDocument.CV,
        nom_original="CV.pdf",
        contenu=b"%PDF-1.4 test",
        type_mime="application/pdf",
        telechargeur_id=str(telechargeur_id),
    )


async def test_executer_televerse_et_sauvegarde():
    """Vérifie le flux nominal : téléversement puis sauvegarde du document."""
    telechargeur_id = uuid4()
    candidature = _candidature(telechargeur_id)

    candidature_repository = AsyncMock()
    candidature_repository.obtenir_par_id = AsyncMock(return_value=candidature)
    candidature_repository.sauvegarder_document = AsyncMock(side_effect=lambda doc: doc)

    storage_port = AsyncMock(spec_set=["televerser", "generer_url_temporaire"])
    storage_port.televerser = AsyncMock(return_value="documents/xxx/CV.pdf")
    storage_port.generer_url_temporaire = AsyncMock(
        return_value="https://minio/presigned/CV.pdf"
    )

    use_case = _build_use_case(candidature_repository, storage_port)

    resultat = await use_case.executer(_donnees(candidature.id, telechargeur_id))

    storage_port.televerser.assert_awaited_once_with(
        fichier=b"%PDF-1.4 test",
        nom_original="CV.pdf",
        categorie=CategorieFichier.DOCUMENT,
        proprietaire_id=telechargeur_id,
    )

    candidature_repository.sauvegarder_document.assert_awaited_once()
    document_sauvegarde = candidature_repository.sauvegarder_document.await_args.args[0]
    assert document_sauvegarde.candidature_id == candidature.id
    assert document_sauvegarde.type_document == TypeDocument.CV
    assert document_sauvegarde.telechargeur_id == telechargeur_id

    assert resultat.id == str(document_sauvegarde.id)
    assert resultat.type_document == TypeDocument.CV


async def test_executer_candidature_introuvable():
    """Vérifie qu'une candidature inexistante remonte CandidatureIntrouvableError."""
    candidature_repository = AsyncMock()
    candidature_repository.obtenir_par_id = AsyncMock(return_value=None)

    use_case = _build_use_case(candidature_repository, AsyncMock())

    with pytest.raises(CandidatureIntrouvableError):
        await use_case.executer(_donnees(uuid4(), uuid4()))


async def test_executer_refuse_si_non_proprietaire():
    """Vérifie qu'un téléchargeur non propriétaire est refusé."""
    proprietaire_id = uuid4()
    candidature = _candidature(proprietaire_id)
    intru_id = uuid4()

    candidature_repository = AsyncMock()
    candidature_repository.obtenir_par_id = AsyncMock(return_value=candidature)

    storage_port = AsyncMock()

    use_case = _build_use_case(candidature_repository, storage_port)

    with pytest.raises(AutorisationRefuseeError):
        await use_case.executer(_donnees(candidature.id, intru_id))

    storage_port.televerser.assert_not_awaited()
