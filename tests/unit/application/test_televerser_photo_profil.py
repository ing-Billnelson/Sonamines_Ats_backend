"""Tests unitaires du use case TeleverserPhotoProfilUseCase."""

from datetime import datetime
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.application.use_cases.televerser_photo_profil import TeleverserPhotoProfilUseCase
from src.domain.entities import Candidat
from src.domain.enums import CanalNotification, CategorieFichier, StatutCompte
from src.domain.exceptions import AutorisationRefuseeError, UtilisateurIntrouvableError
from src.domain.value_objects import Email


def _candidat(photo_url=None) -> Candidat:
    """Construit une entité candidat."""
    return Candidat(
        id=uuid4(),
        email=Email("candidat@test.com"),
        telephone=None,
        mot_de_passe_hash="hash",
        nom="Diop",
        prenom="Amadou",
        statut=StatutCompte.ACTIF,
        canal_validation=CanalNotification.EMAIL,
        email_verifie=True,
        telephone_verifie=False,
        date_creation=datetime.utcnow(),
        date_derniere_connexion=None,
        date_modification=None,
        photo_url=photo_url,
    )


def _build_use_case(utilisateur_repository, storage_port) -> TeleverserPhotoProfilUseCase:
    """Construit le use case avec des ports injectés."""
    return TeleverserPhotoProfilUseCase(
        utilisateur_repository=utilisateur_repository,
        storage_port=storage_port,
    )


async def test_executer_televerse_nouvelle_photo():
    """Vérifie le flux nominal : téléversement puis mise à jour du candidat."""
    candidat = _candidat()

    utilisateur_repository = AsyncMock()
    utilisateur_repository.obtenir_candidat_par_id = AsyncMock(return_value=candidat)
    utilisateur_repository.sauvegarder_candidat = AsyncMock(side_effect=lambda c: c)

    storage_port = AsyncMock(spec_set=["televerser", "supprimer"])
    storage_port.televerser = AsyncMock(return_value="photos/xxx/photo.jpg")
    storage_port.supprimer = AsyncMock(return_value=True)

    use_case = _build_use_case(utilisateur_repository, storage_port)

    resultat = await use_case.executer(
        candidat_id=str(candidat.id),
        fichier=b"image-bytes",
        nom_original="photo.jpg",
    )

    storage_port.televerser.assert_awaited_once_with(
        fichier=b"image-bytes",
        nom_original="photo.jpg",
        categorie=CategorieFichier.PHOTO,
        proprietaire_id=candidat.id,
    )

    # Pas d'ancienne photo → aucune suppression
    storage_port.supprimer.assert_not_awaited()

    assert candidat.photo_url == "photos/xxx/photo.jpg"
    assert resultat.photo_url == "photos/xxx/photo.jpg"
    utilisateur_repository.sauvegarder_candidat.assert_awaited_once()


async def test_executer_supprime_ancienne_photo():
    """Vérifie que l'ancienne photo est supprimée avant le téléversement."""
    candidat = _candidat(photo_url="photos/ancienne.jpg")

    utilisateur_repository = AsyncMock()
    utilisateur_repository.obtenir_candidat_par_id = AsyncMock(return_value=candidat)
    utilisateur_repository.sauvegarder_candidat = AsyncMock(side_effect=lambda c: c)

    storage_port = AsyncMock(spec_set=["televerser", "supprimer"])
    storage_port.televerser = AsyncMock(return_value="photos/nouvelle.jpg")
    storage_port.supprimer = AsyncMock(return_value=True)

    use_case = _build_use_case(utilisateur_repository, storage_port)

    await use_case.executer(
        candidat_id=str(candidat.id),
        fichier=b"image-bytes",
        nom_original="photo.jpg",
    )

    storage_port.supprimer.assert_awaited_once_with(
        "photos/ancienne.jpg", CategorieFichier.PHOTO
    )
    assert candidat.photo_url == "photos/nouvelle.jpg"


async def test_executer_utilisateur_introuvable():
    """Vérifie qu'un candidat inexistant remonte UtilisateurIntrouvableError."""
    utilisateur_repository = AsyncMock()
    utilisateur_repository.obtenir_candidat_par_id = AsyncMock(return_value=None)

    use_case = _build_use_case(utilisateur_repository, AsyncMock())

    with pytest.raises(UtilisateurIntrouvableError):
        await use_case.executer(candidat_id=str(uuid4()), fichier=b"x", nom_original="p.jpg")


async def test_executer_refuse_si_pas_un_candidat():
    """Vérifie qu'un utilisateur non candidat est refusé."""
    utilisateur_repository = AsyncMock()
    utilisateur_repository.obtenir_candidat_par_id = AsyncMock(return_value=object())

    storage_port = AsyncMock()

    use_case = _build_use_case(utilisateur_repository, storage_port)

    with pytest.raises(AutorisationRefuseeError):
        await use_case.executer(candidat_id=str(uuid4()), fichier=b"x", nom_original="p.jpg")
