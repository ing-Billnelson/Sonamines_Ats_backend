"""DTOs pour la gestion des offres."""

from dataclasses import dataclass
from typing import Optional

from ...domain.entities.offre import StatutOffre
from ...domain.enums import TypeContrat, TypeOffre, TypeStage


@dataclass
class CreerOffreDTO:
    """DTO pour la création d'une offre."""

    titre: str
    description: str
    type_offre: TypeOffre
    lieu: str
    type_contrat: Optional[TypeContrat] = None  # Pour les emplois
    type_stage: Optional[TypeStage] = None  # Pour les stages
    date_limite_candidature: Optional[str] = None  # ISO format
    salaire_min: Optional[float] = None
    salaire_max: Optional[float] = None
    competences_requises: Optional[list[str]] = None
    experience_requise: Optional[str] = None


@dataclass
class ModifierOffreDTO:
    """DTO pour la modification d'une offre."""

    offre_id: str  # UUID en string
    titre: Optional[str] = None
    description: Optional[str] = None
    date_limite_candidature: Optional[str] = None  # ISO format
    lieu: Optional[str] = None
    salaire_min: Optional[float] = None
    salaire_max: Optional[float] = None
    competences_requises: Optional[list[str]] = None
    experience_requise: Optional[str] = None


@dataclass
class OffreDTO:
    """DTO de sortie pour les informations d'offre."""

    id: str
    numero_reference: str
    titre: str
    description: str
    type_offre: TypeOffre
    type_contrat: Optional[TypeContrat]
    type_stage: Optional[TypeStage]
    statut: StatutOffre
    date_limite_candidature: Optional[str]  # ISO format
    lieu: str
    salaire_min: Optional[float]
    salaire_max: Optional[float]
    competences_requises: list[str]
    experience_requise: Optional[str]
    createur_nom_complet: str
    date_creation: str  # ISO format
    date_publication: Optional[str] = None  # ISO format
    date_cloture: Optional[str] = None  # ISO format
    nombre_candidatures: Optional[int] = None  # Compteur pour l'affichage


@dataclass
class RechercherOffresDTO:
    """DTO pour les critères de recherche d'offres."""

    texte: Optional[str] = None
    type_offre: Optional[TypeOffre] = None
    type_contrat: Optional[TypeContrat] = None
    type_stage: Optional[TypeStage] = None
    lieu: Optional[str] = None
    competences: Optional[list[str]] = None
    salaire_min: Optional[float] = None
    salaire_max: Optional[float] = None
    limit: int = 20
    offset: int = 0