"""Tests unitaires du use case RechercherOffresUseCase."""

from unittest.mock import AsyncMock, Mock

import pytest

from src.application.use_cases.rechercher_offres import RechercherOffresUseCase
from src.application.dto import RechercherOffresDTO
from src.domain.exceptions import RechercheIndisponibleError


def _fake_hit() -> dict:
    """Retourne un document Elasticsearch simulé pour une offre."""
    return {
        "id": "66666666-6666-6666-6666-666666666666",
        "numero_reference": "OFF-2026-ABC123",
        "titre": "Ingénieur Minier Junior",
        "description": "Rejoignez SONAMINES pour un poste d'ingénieur minier.",
        "type_offre": "EMPLOI",
        "type_contrat": "CDI",
        "type_stage": None,
        "statut": "OUVERTE",
        "lieu": "Dakar",
        "salaire_min": 800000,
        "salaire_max": 1200000,
        "competences_requises": ["geologie", "python"],
        "experience_requise": "2-5 ans",
        "date_creation": "2026-08-12T10:00:00",
        "date_publication": "2026-08-12T10:00:00",
        "date_limite_candidature": "2026-09-30T00:00:00",
        "date_cloture": None,
    }


def _build_use_case(search_port) -> RechercherOffresUseCase:
    """Construit le use case avec un port de recherche injecté."""
    return RechercherOffresUseCase(
        search_port=search_port,
        offre_repository=Mock(),
    )


async def test_executer_delegue_au_port_de_recherche():
    """Vérifie que executer() délègue à search_port et convertit les hits."""
    search_port = AsyncMock()
    search_port.rechercher_offres = AsyncMock(return_value=[_fake_hit(), _fake_hit()])

    use_case = _build_use_case(search_port)
    donnees = RechercherOffresDTO(
        texte="minier",
        type_offre=None,
        lieu=None,
        limit=10,
        offset=0,
    )

    resultats = await use_case.executer(donnees)

    # Le port est appelé avec les critères (texte seul, autres vides exclus)
    search_port.rechercher_offres.assert_awaited_once_with(
        criteres={"texte": "minier"},
        limit=10,
        offset=0,
    )

    assert len(resultats) == 2
    dto = resultats[0]
    assert dto.id == _fake_hit()["id"]
    assert dto.titre == "Ingénieur Minier Junior"
    assert dto.type_offre.value == "EMPLOI"
    assert dto.type_contrat.value == "CDI"
    assert dto.statut.value == "OUVERTE"
    assert dto.competences_requises == ["geologie", "python"]


async def test_executer_convertit_les_enums():
    """Vérifie la conversion des enums et des valeurs optionnelles."""
    search_port = AsyncMock()
    search_port.rechercher_offres = AsyncMock(return_value=[_fake_hit()])

    use_case = _build_use_case(search_port)
    resultats = await use_case.executer(RechercherOffresDTO(texte="minier"))

    dto = resultats[0]
    assert dto.type_stage is None
    assert dto.salaire_min == 800000
    assert dto.date_cloture is None
    assert dto.createur_nom_complet == ""


async def test_executer_propage_recherche_indisponible():
    """Vérifie qu'une erreur du port remonte en RechercheIndisponibleError (503)."""
    search_port = AsyncMock()
    search_port.rechercher_offres = AsyncMock(
        side_effect=RechercheIndisponibleError("ES hors ligne")
    )

    use_case = _build_use_case(search_port)

    with pytest.raises(RechercheIndisponibleError):
        await use_case.executer(RechercherOffresDTO(texte="minier"))


async def test_executer_filtre_les_criteres_non_renseignes():
    """Vérifie que les critères vides ne sont pas transmis au port."""
    search_port = AsyncMock()
    search_port.rechercher_offres = AsyncMock(return_value=[])

    use_case = _build_use_case(search_port)
    await use_case.executer(RechercherOffresDTO())

    search_port.rechercher_offres.assert_awaited_once_with(
        criteres={},
        limit=20,
        offset=0,
    )
