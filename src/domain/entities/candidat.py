"""Entité candidat."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from ..enums import CanalNotification, Disponibilite, NiveauAcademique, Sexe, StatutCompte
from ..value_objects import Email, NumeroTelephone
from .utilisateur import Utilisateur


@dataclass
class Candidat(Utilisateur):
    """Entité représentant un candidat à l'emploi ou au stage."""

    photo_url: Optional[str] = None  # URL de la photo de profil (facultative)
    linkedin_url: Optional[str] = None  # URL du profil LinkedIn (facultative)
    adresse: Optional[str] = None  # Adresse du candidat (facultative)
    competences: list[str] = field(default_factory=list)  # Compétences du candidat

    # Champs du profil étendu pour la recherche multicritère
    sexe: Optional[Sexe] = None
    date_naissance: Optional[datetime] = None
    nationalite: Optional[str] = None
    region_origine: Optional[str] = None
    region_residence: Optional[str] = None
    langues_parlees: list[str] = field(default_factory=list)
    disponibilite: Optional[Disponibilite] = None
    niveau_academique: Optional[NiveauAcademique] = None
    domaine_formation: Optional[str] = None
    specialite: Optional[str] = None

    @classmethod
    def creer_nouveau(
        cls,
        email: Email,
        telephone: Optional[NumeroTelephone],
        mot_de_passe_hash: str,
        nom: str,
        prenom: str,
        canal_validation: CanalNotification,
    ) -> "Candidat":
        """Crée un nouveau candidat avec les valeurs par défaut."""
        candidat = cls(
            id=uuid4(),
            email=email,
            telephone=telephone,
            mot_de_passe_hash=mot_de_passe_hash,
            nom=nom,
            prenom=prenom,
            statut=StatutCompte.EN_ATTENTE_VALIDATION,
            canal_validation=canal_validation,
            email_verifie=False,
            telephone_verifie=False,
            date_creation=datetime.utcnow(),
            date_derniere_connexion=None,
            date_modification=None,
            photo_url=None,
        )
        candidat.generer_code_validation()
        return candidat

    def definir_photo_profil(self, photo_url: str) -> None:
        """Définit l'URL de la photo de profil du candidat."""
        self.photo_url = photo_url
        self.date_modification = datetime.utcnow()

    def supprimer_photo_profil(self) -> None:
        """Supprime la photo de profil du candidat."""
        self.photo_url = None
        self.date_modification = datetime.utcnow()

    def a_photo_profil(self) -> bool:
        """Vérifie si le candidat a une photo de profil."""
        return self.photo_url is not None