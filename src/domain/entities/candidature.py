"""Entité candidature."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from ..enums import StatutCandidature
from ..value_objects import NumeroReference


@dataclass
class Candidature:
    """Entité représentant une candidature d'un candidat."""

    id: UUID
    numero_reference: NumeroReference
    candidat_id: UUID
    offre_id: Optional[UUID]  # None pour candidature spontanée
    statut: StatutCandidature
    date_soumission: datetime
    date_derniere_modification: datetime
    message_motivation: Optional[str] = None
    notes_internes: Optional[str] = None  # Notes ajoutées par les RH
    score_eligibilite: Optional[float] = None  # Score d'éligibilité (0-100)
    documents: list["Document"] = field(default_factory=list)

    @classmethod
    def creer_nouvelle(
        cls,
        candidat_id: UUID,
        message_motivation: Optional[str] = None,
        offre_id: Optional[UUID] = None,
    ) -> "Candidature":
        """Crée une nouvelle candidature."""
        numero_ref = NumeroReference.generer_candidature()

        return cls(
            id=uuid4(),
            numero_reference=numero_ref,
            candidat_id=candidat_id,
            offre_id=offre_id,
            statut=StatutCandidature.RECUE,
            message_motivation=message_motivation,
            date_soumission=datetime.utcnow(),
            date_derniere_modification=datetime.utcnow(),
        )

    def changer_statut(self, nouveau_statut: StatutCandidature) -> None:
        """Change le statut de la candidature."""
        if self.statut.is_terminal:
            raise ValueError(
                f"Impossible de changer le statut d'une candidature {self.statut}"
            )

        self.statut = nouveau_statut
        self.date_derniere_modification = datetime.utcnow()

    def ajouter_notes_internes(self, notes: str) -> None:
        """Ajoute des notes internes à la candidature (usage RH)."""
        self.notes_internes = notes
        self.date_derniere_modification = datetime.utcnow()

    def est_spontanee(self) -> bool:
        """Vérifie si la candidature est spontanée."""
        return self.offre_id is None

    def peut_etre_modifiee(self) -> bool:
        """Vérifie si la candidature peut encore être modifiée."""
        return not self.statut.is_terminal

    def est_complete(self) -> bool:
        """Vérifie si le dossier de candidature est complet."""
        # TODO: Implémenter la logique de vérification des documents requis
        return len(self.documents) > 0