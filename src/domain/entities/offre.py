"""Entité offre d'emploi ou de stage."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from ..enums import TypeContrat, TypeOffre, TypeStage
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