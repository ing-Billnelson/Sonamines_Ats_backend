"""Repository PostgreSQL pour les utilisateurs."""

from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ....domain.entities import Candidat, AdministrateurRH, SuperAdministrateur, Utilisateur
from ....domain.ports import UtilisateurRepository
from ....domain.value_objects import Email, NumeroTelephone
from ..models import (
    CandidatModel,
    AdministrateurRHModel,
    SuperAdministrateurModel,
    UtilisateurModel,
)


class PostgresUtilisateurRepository(UtilisateurRepository):
    """Repository PostgreSQL pour la gestion des utilisateurs."""

    def __init__(self, session: AsyncSession):
        self._session = session

    def _model_vers_entite(self, model: UtilisateurModel) -> Utilisateur:
        """Convertit un modèle SQLAlchemy en entité domaine."""
        kwargs = {
            "id": model.id,
            "email": Email(model.email),
            "telephone": NumeroTelephone(model.telephone) if model.telephone else None,
            "mot_de_passe_hash": model.mot_de_passe_hash,
            "nom": model.nom,
            "prenom": model.prenom,
            "statut": model.statut,
            "canal_validation": model.canal_validation,
            "email_verifie": model.email_verifie,
            "telephone_verifie": model.telephone_verifie,
            "code_validation": model.code_validation,
            "code_validation_expiration": model.code_validation_expiration,
            "code_reinitialisation": model.code_reinitialisation,
            "code_reinitialisation_expiration": model.code_reinitialisation_expiration,
            "date_creation": model.date_creation,
            "date_derniere_connexion": model.date_derniere_connexion,
            "date_modification": model.date_modification,
        }

        if model.type_utilisateur == "candidat":
            return Candidat(
                **kwargs,
                photo_url=model.photo_url,
                linkedin_url=model.linkedin_url,
                adresse=model.adresse,
                competences=model.competences,
                sexe=model.sexe,
                date_naissance=model.date_naissance,
                nationalite=model.nationalite,
                region_origine=model.region_origine,
                region_residence=model.region_residence,
                langues_parlees=model.langues_parlees,
                disponibilite=model.disponibilite,
                niveau_academique=model.niveau_academique,
                domaine_formation=model.domaine_formation,
                specialite=model.specialite,
            )
        elif model.type_utilisateur == "administrateur_rh":
            return AdministrateurRH(**kwargs)
        elif model.type_utilisateur == "super_administrateur":
            return SuperAdministrateur(**kwargs)

        raise ValueError(f"Type d'utilisateur non supporté: {model.type_utilisateur}")

    async def sauvegarder_candidat(self, candidat: Candidat) -> Candidat:
        """Sauvegarde un candidat et retourne l'entité mise à jour."""
        query = select(CandidatModel).where(CandidatModel.id == candidat.id)
        result = await self._session.execute(query)
        model = result.scalar_one_or_none()

        if model is None:
            model = CandidatModel(
                id=candidat.id,
                email=str(candidat.email),
                telephone=str(candidat.telephone) if candidat.telephone else None,
                mot_de_passe_hash=candidat.mot_de_passe_hash,
                nom=candidat.nom,
                prenom=candidat.prenom,
                statut=candidat.statut,
                canal_validation=candidat.canal_validation,
                email_verifie=candidat.email_verifie,
                telephone_verifie=candidat.telephone_verifie,
                code_validation=candidat.code_validation,
                code_validation_expiration=candidat.code_validation_expiration,
                code_reinitialisation=candidat.code_reinitialisation,
                code_reinitialisation_expiration=candidat.code_reinitialisation_expiration,
                date_creation=candidat.date_creation,
                date_derniere_connexion=candidat.date_derniere_connexion,
                date_modification=candidat.date_modification,
                photo_url=candidat.photo_url,
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
            )
            self._session.add(model)
        else:
            model.email = str(candidat.email)
            model.telephone = str(candidat.telephone) if candidat.telephone else None
            model.mot_de_passe_hash = candidat.mot_de_passe_hash
            model.nom = candidat.nom
            model.prenom = candidat.prenom
            model.statut = candidat.statut
            model.canal_validation = candidat.canal_validation
            model.email_verifie = candidat.email_verifie
            model.telephone_verifie = candidat.telephone_verifie
            model.code_validation = candidat.code_validation
            model.code_validation_expiration = candidat.code_validation_expiration
            model.code_reinitialisation = candidat.code_reinitialisation
            model.code_reinitialisation_expiration = candidat.code_reinitialisation_expiration
            model.date_creation = candidat.date_creation
            model.date_derniere_connexion = candidat.date_derniere_connexion
            model.date_modification = candidat.date_modification
            model.photo_url = candidat.photo_url
            model.linkedin_url = candidat.linkedin_url
            model.adresse = candidat.adresse
            model.competences = candidat.competences
            model.sexe = candidat.sexe
            model.date_naissance = candidat.date_naissance
            model.nationalite = candidat.nationalite
            model.region_origine = candidat.region_origine
            model.region_residence = candidat.region_residence
            model.langues_parlees = candidat.langues_parlees
            model.disponibilite = candidat.disponibilite
            model.niveau_academique = candidat.niveau_academique
            model.domaine_formation = candidat.domaine_formation
            model.specialite = candidat.specialite

        await self._session.flush()
        return self._model_vers_entite(model)

    async def sauvegarder_admin_rh(self, admin: AdministrateurRH) -> AdministrateurRH:
        """Sauvegarde un administrateur RH et retourne l'entité mise à jour."""
        query = select(AdministrateurRHModel).where(AdministrateurRHModel.id == admin.id)
        result = await self._session.execute(query)
        model = result.scalar_one_or_none()

        if model is None:
            model = AdministrateurRHModel(
                id=admin.id,
                email=str(admin.email),
                telephone=str(admin.telephone) if admin.telephone else None,
                mot_de_passe_hash=admin.mot_de_passe_hash,
                nom=admin.nom,
                prenom=admin.prenom,
                statut=admin.statut,
                canal_validation=admin.canal_validation,
                email_verifie=admin.email_verifie,
                telephone_verifie=admin.telephone_verifie,
                code_validation=admin.code_validation,
                code_validation_expiration=admin.code_validation_expiration,
                code_reinitialisation=admin.code_reinitialisation,
                code_reinitialisation_expiration=admin.code_reinitialisation_expiration,
                date_creation=admin.date_creation,
                date_derniere_connexion=admin.date_derniere_connexion,
                date_modification=admin.date_modification,
            )
            self._session.add(model)
        else:
            model.email = str(admin.email)
            model.telephone = str(admin.telephone) if admin.telephone else None
            model.mot_de_passe_hash = admin.mot_de_passe_hash
            model.nom = admin.nom
            model.prenom = admin.prenom
            model.statut = admin.statut
            model.canal_validation = admin.canal_validation
            model.email_verifie = admin.email_verifie
            model.telephone_verifie = admin.telephone_verifie
            model.code_validation = admin.code_validation
            model.code_validation_expiration = admin.code_validation_expiration
            model.code_reinitialisation = admin.code_reinitialisation
            model.code_reinitialisation_expiration = admin.code_reinitialisation_expiration
            model.date_creation = admin.date_creation
            model.date_derniere_connexion = admin.date_derniere_connexion
            model.date_modification = admin.date_modification

        await self._session.flush()
        return self._model_vers_entite(model)

    async def sauvegarder_super_admin(
        self, admin: SuperAdministrateur
    ) -> SuperAdministrateur:
        """Sauvegarde un super administrateur et retourne l'entité mise à jour."""
        query = select(SuperAdministrateurModel).where(SuperAdministrateurModel.id == admin.id)
        result = await self._session.execute(query)
        model = result.scalar_one_or_none()

        if model is None:
            model = SuperAdministrateurModel(
                id=admin.id,
                email=str(admin.email),
                telephone=str(admin.telephone) if admin.telephone else None,
                mot_de_passe_hash=admin.mot_de_passe_hash,
                nom=admin.nom,
                prenom=admin.prenom,
                statut=admin.statut,
                canal_validation=admin.canal_validation,
                email_verifie=admin.email_verifie,
                telephone_verifie=admin.telephone_verifie,
                code_validation=admin.code_validation,
                code_validation_expiration=admin.code_validation_expiration,
                code_reinitialisation=admin.code_reinitialisation,
                code_reinitialisation_expiration=admin.code_reinitialisation_expiration,
                date_creation=admin.date_creation,
                date_derniere_connexion=admin.date_derniere_connexion,
                date_modification=admin.date_modification,
            )
            self._session.add(model)
        else:
            model.email = str(admin.email)
            model.telephone = str(admin.telephone) if admin.telephone else None
            model.mot_de_passe_hash = admin.mot_de_passe_hash
            model.nom = admin.nom
            model.prenom = admin.prenom
            model.statut = admin.statut
            model.canal_validation = admin.canal_validation
            model.email_verifie = admin.email_verifie
            model.telephone_verifie = admin.telephone_verifie
            model.code_validation = admin.code_validation
            model.code_validation_expiration = admin.code_validation_expiration
            model.code_reinitialisation = admin.code_reinitialisation
            model.code_reinitialisation_expiration = admin.code_reinitialisation_expiration
            model.date_creation = admin.date_creation
            model.date_derniere_connexion = admin.date_derniere_connexion
            model.date_modification = admin.date_modification

        await self._session.flush()
        return self._model_vers_entite(model)

    async def obtenir_par_id(self, utilisateur_id: UUID) -> Optional[Utilisateur]:
        """Récupère un utilisateur par son ID."""
        query = select(UtilisateurModel).where(UtilisateurModel.id == utilisateur_id)
        result = await self._session.execute(query)
        model = result.scalar_one_or_none()
        
        if not model:
            return None

        return self._model_vers_entite(model)

    async def obtenir_par_email(self, email: Email) -> Optional[Utilisateur]:
        """Récupère un utilisateur par son email."""
        query = select(UtilisateurModel).where(UtilisateurModel.email == str(email))
        result = await self._session.execute(query)
        model = result.scalar_one_or_none()
        
        if not model:
            return None

        return self._model_vers_entite(model)

    async def obtenir_candidat_par_id(self, candidat_id: UUID) -> Optional[Candidat]:
        """Récupère un candidat spécifiquement par son ID."""
        query = select(CandidatModel).where(CandidatModel.id == candidat_id)
        result = await self._session.execute(query)
        model = result.scalar_one_or_none()
        
        if not model:
            return None

        return self._model_vers_entite(model)

    async def obtenir_admin_rh_par_id(
        self, admin_id: UUID
    ) -> Optional[AdministrateurRH]:
        """Récupère un administrateur RH par son ID."""
        query = select(AdministrateurRHModel).where(AdministrateurRHModel.id == admin_id)
        result = await self._session.execute(query)
        model = result.scalar_one_or_none()
        
        if not model:
            return None
        
        # TODO: Implémenter la conversion modèle -> entité
        return None

    async def obtenir_super_admin_par_id(
        self, admin_id: UUID
    ) -> Optional[SuperAdministrateur]:
        """Récupère un super administrateur par son ID."""
        query = select(SuperAdministrateurModel).where(SuperAdministrateurModel.id == admin_id)
        result = await self._session.execute(query)
        model = result.scalar_one_or_none()
        
        if not model:
            return None
        
        # TODO: Implémenter la conversion modèle -> entité
        return None

    async def email_existe(self, email: Email) -> bool:
        """Vérifie si un email existe déjà dans le système."""
        query = select(UtilisateurModel.id).where(UtilisateurModel.email == str(email))
        result = await self._session.execute(query)
        return result.scalar_one_or_none() is not None

    async def supprimer(self, utilisateur_id: UUID) -> bool:
        """Supprime un utilisateur du système."""
        query = select(UtilisateurModel).where(UtilisateurModel.id == utilisateur_id)
        result = await self._session.execute(query)
        model = result.scalar_one_or_none()
        
        if not model:
            return False
        
        await self._session.delete(model)
        await self._session.commit()
        return True