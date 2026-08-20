"""Conversion des entités candidat/formation/expérience en DTOs de profil."""

from ...domain.entities import Candidat
from ...domain.ports import ProfilCandidatRepository
from ..dto import ExperienceDTO, FormationDTO, UtilisateurDTO


async def convertir_candidat_profil_en_dto(
    candidat: Candidat,
    profil_candidat_repository: ProfilCandidatRepository,
) -> UtilisateurDTO:
    """Convertit un candidat en DTO complet avec formations et expériences."""
    formations = await profil_candidat_repository.obtenir_formations_candidat(
        candidat.id
    )
    experiences = await profil_candidat_repository.obtenir_experiences_candidat(
        candidat.id
    )

    return UtilisateurDTO(
        id=str(candidat.id),
        email=str(candidat.email),
        telephone=str(candidat.telephone) if candidat.telephone else None,
        nom=candidat.nom,
        prenom=candidat.prenom,
        nom_complet=candidat.nom_complet,
        statut=candidat.statut,
        canal_validation=candidat.canal_validation,
        email_verifie=candidat.email_verifie,
        telephone_verifie=candidat.telephone_verifie,
        date_creation=candidat.date_creation.isoformat(),
        date_derniere_connexion=(
            candidat.date_derniere_connexion.isoformat()
            if candidat.date_derniere_connexion
            else None
        ),
        photo_url=candidat.photo_url,
        role="candidat",
        linkedin_url=candidat.linkedin_url,
        adresse=candidat.adresse,
        competences=candidat.competences,
        sexe=candidat.sexe,
        date_naissance=candidat.date_naissance,
        nationalite=candidat.nationalite,
        region_origine=candidat.region_origine,
        region_residence=candidat.region_residence,
        langues_parlees=candidat.langues_parlees,
        disponibilite=candidat.disponibilite,
        niveau_academique=candidat.niveau_academique,
        domaine_formation=candidat.domaine_formation,
        specialite=candidat.specialite,
        formations=[_formation_en_dto(f) for f in formations],
        experiences=[_experience_en_dto(e) for e in experiences],
    )


def formation_en_dto(formation) -> FormationDTO:
    return FormationDTO(
        id=str(formation.id),
        etablissement=formation.etablissement,
        diplome=formation.diplome,
        annee_debut=formation.annee_debut,
        annee_fin=formation.annee_fin,
    )


def experience_en_dto(experience) -> ExperienceDTO:
    return ExperienceDTO(
        id=str(experience.id),
        entreprise=experience.entreprise,
        poste=experience.poste,
        date_debut=experience.date_debut.isoformat(),
        date_fin=(
            experience.date_fin.isoformat() if experience.date_fin else None
        ),
        description=experience.description,
    )


# Alias privés pour compatibilité
_formation_en_dto = formation_en_dto
_experience_en_dto = experience_en_dto
