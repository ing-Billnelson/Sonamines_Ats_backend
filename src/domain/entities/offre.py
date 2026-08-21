"""Entité offre d'emploi ou de stage."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from ..enums import (
    Disponibilite,
    NiveauAcademique,
    TypeContrat,
    TypeOffre,
    TypeStage,
    ordre_niveau_academique,
)
from ..value_objects import NumeroReference


class StatutOffre(str, Enum):
    """Statuts possibles d'une offre."""

    BROUILLON = "BROUILLON"
    OUVERTE = "OUVERTE"
    CLOTUREE = "CLOTUREE"
    ARCHIVEE = "ARCHIVEE"

    def __str__(self) -> str:
        return self.value

    @property
    def is_active(self) -> bool:
        """Vérifie si l'offre est active (candidatures possibles)."""
        return self == StatutOffre.OUVERTE


@dataclass
class Offre:
    """Entité représentant une offre d'emploi ou de stage."""

    id: UUID
    numero_reference: NumeroReference
    titre: str
    description: str
    type_offre: TypeOffre
    type_contrat: Optional[TypeContrat]  # Seulement pour les emplois
    type_stage: Optional[TypeStage]  # Seulement pour les stages
    statut: StatutOffre
    date_limite_candidature: Optional[datetime]
    lieu: str
    salaire_min: Optional[float]
    salaire_max: Optional[float]
    competences_requises: list[str]
    experience_requise: Optional[str]
    createur_id: UUID  # ID de l'administrateur RH qui a créé l'offre
    date_creation: datetime
    date_publication: Optional[datetime] = None
    date_cloture: Optional[datetime] = None
    date_modification: Optional[datetime] = None

    # Critères d'éligibilité (utilisés pour scorer les candidatures)
    eligibilite_activee: bool = False
    niveau_academique_minimum: Optional[NiveauAcademique] = None
    langues_requises: list[str] = field(default_factory=list)
    disponibilite_requise: Optional[Disponibilite] = None

    @classmethod
    def creer_nouvelle(
        cls,
        titre: str,
        description: str,
        type_offre: TypeOffre,
        lieu: str,
        createur_id: UUID,
        type_contrat: Optional[TypeContrat] = None,
        type_stage: Optional[TypeStage] = None,
        date_limite_candidature: Optional[datetime] = None,
        salaire_min: Optional[float] = None,
        salaire_max: Optional[float] = None,
        competences_requises: Optional[list[str]] = None,
        experience_requise: Optional[str] = None,
        eligibilite_activee: bool = False,
        niveau_academique_minimum: Optional[NiveauAcademique] = None,
        langues_requises: Optional[list[str]] = None,
        disponibilite_requise: Optional[Disponibilite] = None,
    ) -> "Offre":
        """Crée une nouvelle offre avec les valeurs par défaut."""
        if type_offre == TypeOffre.EMPLOI and type_contrat is None:
            raise ValueError("Le type de contrat est requis pour les emplois")
        if type_offre == TypeOffre.STAGE and type_stage is None:
            raise ValueError("Le type de stage est requis pour les stages")

        numero_ref = NumeroReference.generer_offre(type_offre.value)

        return cls(
            id=uuid4(),
            numero_reference=numero_ref,
            titre=titre,
            description=description,
            type_offre=type_offre,
            type_contrat=type_contrat,
            type_stage=type_stage,
            statut=StatutOffre.BROUILLON,
            date_limite_candidature=date_limite_candidature,
            lieu=lieu,
            salaire_min=salaire_min,
            salaire_max=salaire_max,
            competences_requises=competences_requises or [],
            experience_requise=experience_requise,
            createur_id=createur_id,
            date_creation=datetime.utcnow(),
            eligibilite_activee=eligibilite_activee,
            niveau_academique_minimum=niveau_academique_minimum,
            langues_requises=langues_requises or [],
            disponibilite_requise=disponibilite_requise,
        )

    def publier(self) -> None:
        """Publie l'offre (la rend visible aux candidats)."""
        if self.statut != StatutOffre.BROUILLON:
            raise ValueError("Seules les offres en brouillon peuvent être publiées")

        self.statut = StatutOffre.OUVERTE
        self.date_publication = datetime.utcnow()
        self.date_modification = datetime.utcnow()

    def cloturer(self) -> None:
        """Clôture l'offre (arrête l'acceptation des candidatures)."""
        if self.statut != StatutOffre.OUVERTE:
            raise ValueError("Seules les offres ouvertes peuvent être clôturées")

        self.statut = StatutOffre.CLOTUREE
        self.date_cloture = datetime.utcnow()
        self.date_modification = datetime.utcnow()

    def archiver(self) -> None:
        """Archive l'offre."""
        if self.statut not in {StatutOffre.CLOTUREE, StatutOffre.OUVERTE}:
            raise ValueError("Seules les offres ouvertes ou clôturées peuvent être archivées")

        self.statut = StatutOffre.ARCHIVEE
        self.date_modification = datetime.utcnow()

    def peut_recevoir_candidatures(self) -> bool:
        """Vérifie si l'offre peut recevoir des candidatures."""
        if not self.statut.is_active:
            return False

        if self.date_limite_candidature is None:
            return True

        return datetime.utcnow() <= self.date_limite_candidature

    def est_expiree(self) -> bool:
        """Vérifie si l'offre est expirée."""
        if self.date_limite_candidature is None:
            return False

        return datetime.utcnow() > self.date_limite_candidature

    def verifier_eligibilite(self, candidat: "Candidat") -> tuple[bool, list[str]]:
        """Vérifie si le candidat satisfait les critères d'éligibilité de l'offre.

        Retourne (True, []) immédiatement si l'éligibilité n'est pas activée,
        sinon (True, []) si tous les critères définis sont satisfaits, ou
        (False, liste des messages décrivant chaque critère manquant).
        """
        if not self.eligibilite_activee:
            return True, []

        manquants: list[str] = []

        # Niveau académique minimum
        if self.niveau_academique_minimum is not None:
            if (
                candidat.niveau_academique is None
                or ordre_niveau_academique(candidat.niveau_academique)
                < ordre_niveau_academique(self.niveau_academique_minimum)
            ):
                manquants.append(
                    f"Niveau académique insuffisant ({self.niveau_academique_minimum.value} requis)"
                )

        # Langues requises (toutes doivent être maîtrisées)
        if self.langues_requises:
            langues_candidat = set(candidat.langues_parlees or [])
            manquantes = [l for l in self.langues_requises if l not in langues_candidat]
            if manquantes:
                manquants.append(f"Langues requises manquantes: {', '.join(manquantes)}")

        # Disponibilité requise
        if self.disponibilite_requise is not None:
            if candidat.disponibilite != self.disponibilite_requise:
                manquants.append(
                    f"Disponibilité requise: {self.disponibilite_requise.value}"
                )

        # Compétences requises (toutes doivent être présentes)
        if self.competences_requises:
            competences_candidat = set(candidat.competences or [])
            manquantes = [
                c for c in self.competences_requises if c not in competences_candidat
            ]
            if manquantes:
                manquants.append(
                    f"Compétences requises manquantes: {', '.join(manquantes)}"
                )

        return len(manquants) == 0, manquants

    def calculer_score_eligibilite(self, candidat: "Candidat") -> float:
        """Calcule un score d'éligibilité sur 100 (0-100).

        FORMULE V1 (arbitraire, ajustable) — ne retourne un score non nul que
        si ``eligibilite_activee`` est True (sinon 0.0).

        Répartition (total 100) :
        - Niveau académique (max 25 pts) : 0 si pas de minimum défini, si le
          candidat est au niveau ou en dessous ; sinon +8.33 pts par niveau
          au-dessus du minimum (25/3), plafonné à 25.
        - Compétences (max 50 pts) :
            (compétences_requises matchées / total_requises) * 35
            + min(nb compétences supplémentaires du candidat hors requises, 5) * 3
          S'il n'y a aucune compétence requise, 35 pts de base + bonus.
        - Disponibilité (max 25 pts) : 25 si le candidat est IMMEDIATE alors
          qu'autre chose était requise (dépassement), 15 si correspond
          exactement, 0 sinon.
        """
        if not self.eligibilite_activee:
            return 0.0

        score = 0.0

        # --- Niveau académique (25 pts max) ---
        if (
            self.niveau_academique_minimum is not None
            and candidat.niveau_academique is not None
        ):
            niveau_candidat = ordre_niveau_academique(candidat.niveau_academique)
            niveau_min = ordre_niveau_academique(self.niveau_academique_minimum)
            ecart = niveau_candidat - niveau_min
            if ecart > 0:
                score += min(ecart * (25 / 3), 25)

        # --- Compétences (50 pts max) ---
        requises = [c for c in (self.competences_requises or []) if c]
        competences_candidat = set(candidat.competences or [])
        if requises:
            matchees = sum(1 for c in requises if c in competences_candidat)
            composante_match = (matchees / len(requises)) * 35
        else:
            composante_match = 35.0
        supplementaires = competences_candidat - set(requises)
        bonus = min(len(supplementaires), 5) * 3
        score += min(composante_match + bonus, 50)

        # --- Disponibilité (25 pts max) ---
        if self.disponibilite_requise is not None:
            if (
                candidat.disponibilite == Disponibilite.IMMEDIATE
                and self.disponibilite_requise != Disponibilite.IMMEDIATE
            ):
                score += 25
            elif candidat.disponibilite == self.disponibilite_requise:
                score += 15

        return round(min(score, 100.0), 2)