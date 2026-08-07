"""DTOs pour les résultats de recherche."""

from dataclasses import dataclass
from typing import Any, Dict, Generic, List, Optional, TypeVar

T = TypeVar("T")


@dataclass
class ResultatRechercheDTO(Generic[T]):
    """DTO générique pour les résultats de recherche paginés."""

    resultats: List[T]
    total: int
    limite: int
    decalage: int
    page_courante: int
    nombre_pages: int
    a_page_suivante: bool
    a_page_precedente: bool


@dataclass
class FacetteRechercheDTO:
    """DTO pour les facettes de recherche (filtres disponibles)."""

    nom: str
    valeurs: List[Dict[str, Any]]  # [{"valeur": "CDI", "compte": 15}, ...]


@dataclass
class ResultatRechercheAvanceeDTO(Generic[T]):
    """DTO pour les résultats de recherche avec facettes et métadonnées."""

    resultats: List[T]
    total: int
    limite: int
    decalage: int
    page_courante: int
    nombre_pages: int
    a_page_suivante: bool
    a_page_precedente: bool
    facettes: List[FacetteRechercheDTO]
    temps_execution_ms: int
    requete_elasticsearch: Optional[Dict[str, Any]] = None  # Pour debugging