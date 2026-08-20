"""DTOs pour la gestion des candidatures."""

from dataclasses import dataclass
from typing import Optional

from ...domain.entities.document import TypeDocument
from ...domain.enums import (
    Disponibilite,
    NiveauAcademique,
    Sexe,
    StatutCandidature,
    TypeOffre,
)


@dataclass
class SoumettreKandidatureDTO:
    """DTO pour la soumission d'une candidature."""

    candidat_id: str  # UUID en string
    message_motivation: Optional[str] = None
    offre_id: Optional[str] = None  # UUID en string, None pour candidature spontanée


@dataclass
class ChangerStatutCandidatureDTO:
    """DTO pour le changement de statut d'une candidature."""

    candidature_id: str  # UUID en string
    nouveau_statut: StatutCandidature
    utilisateur_id: str  # ID de l'utilisateur qui effectue le changement
    commentaire: Optional[str] = None


@dataclass
class AjouterNotesInternesDTO:
    """DTO pour l'ajout de notes internes à une candidature."""

    candidature_id: str  # UUID en string
    notes: str
    utilisateur_id: str  # ID de l'utilisateur qui ajoute les notes


@dataclass
class TeleverserDocumentDTO:
    """DTO pour le téléversement d'un document de candidature."""

    candidature_id: str  # UUID en string
    type_document: TypeDocument
    nom_original: str
    contenu: bytes
    type_mime: str
    telechargeur_id: str  # UUID en string


@dataclass
class DocumentDTO:
    """DTO de sortie pour les informations de document."""

    id: str
    type_document: TypeDocument
    nom_original: str
    taille_octets: int
    type_mime: str
    url_temporaire: Optional[str]  # URL d'accès temporaire
    date_telechargement: str  # ISO format
    telechargeur_nom_complet: str


@dataclass
class HistoriqueStatutDTO:
    """DTO pour l'historique des changements de statut."""

    id: str
    ancien_statut: Optional[StatutCandidature]
    nouveau_statut: StatutCandidature
    commentaire: Optional[str]
    utilisateur_nom_complet: str
    date_changement: str  # ISO format


@dataclass
class CandidatureDTO:
    """DTO de sortie pour les informations de candidature."""

    id: str
    numero_reference: str
    candidat_nom_complet: str
    candidat_email: str
    offre_titre: Optional[str]  # None pour candidature spontanée
    offre_numero_reference: Optional[str]
    statut: StatutCandidature
    message_motivation: Optional[str]  # Optionnel (message libre)
    notes_internes: Optional[str]
    date_soumission: str  # ISO format
    date_derniere_modification: str  # ISO format
    documents: list[DocumentDTO]
    historique: list[HistoriqueStatutDTO]
    est_spontanee: bool
    est_complete: bool


@dataclass
class RechercherCandidaturesDTO:
    """DTO pour les critères de recherche de candidatures."""

    texte: Optional[str] = None
    statut: Optional[StatutCandidature] = None
    offre_id: Optional[str] = None  # UUID en string
    candidat_nom: Optional[str] = None
    date_debut: Optional[str] = None  # ISO format
    date_fin: Optional[str] = None  # ISO format
    spontanee: Optional[bool] = None
    # Critères du profil candidat (dénormalisés dans l'index)
    sexe: Optional[Sexe] = None
    age_min: Optional[int] = None  # Converti en range sur candidat_date_naissance
    age_max: Optional[int] = None  # Converti en range sur candidat_date_naissance
    diplome: Optional[str] = None  # Mappé sur candidat_niveau_academique
    domaine_formation: Optional[str] = None
    niveau_academique: Optional[NiveauAcademique] = None
    specialite: Optional[str] = None
    competences: Optional[list[str]] = None
    region_origine: Optional[str] = None
    region_residence: Optional[str] = None
    langues_parlees: Optional[list[str]] = None
    disponibilite: Optional[Disponibilite] = None
    type_offre: Optional[TypeOffre] = None  # Filtre via offre_type_offre
    limit: int = 20
    offset: int = 0