"""Point d'entrée principal de l'API FastAPI."""

import structlog
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text

from ..domain.exceptions import (
    DomainException,
    FichierTropVolumineuxError,
    FormatFichierNonSupporteError,
    UtilisateurExistantError,
    UtilisateurIntrouvableError,
    OffreIntrouvableError,
    CandidatureIntrouvableError,
    StatutCandidatureInvalideError,
    AuthentificationEchoueeError,
    AutorisationRefuseeError,
    CanalNonVerifieError,
    CandidatureNonEligibleError,
    OffreClotureeError,
)
from ..infrastructure.config import settings
from ..infrastructure.db.session import engine
from .v1.routers import (
    admin_router,
    auth_router,
    candidats_router,
    candidatures_router,
    moi_router,
    notifications_router,
    offres_router,
)

# Configuration du logger
logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestionnaire de cycle de vie de l'application."""
    # Startup
    logger.info("🚀 Démarrage de l'API SONAMINES Candidatures")
    
    # Vérification de la connexion à la base de données
    try:
        # Test de connexion simple
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("✅ Connexion à la base de données PostgreSQL établie", 
                   database_url=settings.database_url.split('@')[1])  # Log sans credentials
    except Exception as e:
        logger.error("❌ Échec de connexion à la base de données", error=str(e))
        raise
    
    logger.info("🗄️ Engine de base de données configuré et prêt", 
               pool_size=engine.pool.size(), 
               max_overflow=engine.pool._max_overflow)
    
    # TODO: Initialiser les autres services externes
    # - Elasticsearch
    # - MinIO
    # - Vérifier les buckets MinIO
    # - Créer les index Elasticsearch si nécessaire
    
    yield
    
    # Shutdown
    logger.info("🛑 Arrêt de l'API SONAMINES Candidatures")
    
    # Fermeture propre du pool de connexions
    logger.info("🔌 Fermeture du pool de connexions de base de données...")
    await engine.dispose()
    logger.info("✅ Pool de connexions fermé proprement")
    
    # TODO: Nettoyer les autres connexions
    # - Fermer les clients ES et MinIO


# Création de l'application FastAPI
app = FastAPI(
    title="SONAMINES - Plateforme de Candidatures",
    description="""
    API de gestion des candidatures à l'emploi et au stage pour SONAMINES SA.
    
    ## Fonctionnalités
    
    * **Authentification** : Création de comptes, validation, connexion JWT
    * **Candidats** : Gestion du profil, soumission de candidatures, téléversement de documents
    * **Offres** : Consultation des offres publiques, recherche multicritère
    * **Administration RH** : Gestion des offres, suivi des candidatures, changement de statuts
    * **Notifications** : Centre de notifications avec envoi email/SMS
    
    ## Architecture
    
    Cette API suit une architecture hexagonale (ports & adapters) avec :
    - **Domain** : Entités métier, règles de gestion, ports
    - **Application** : Use cases, DTOs
    - **Infrastructure** : Adapters PostgreSQL, Elasticsearch, MinIO, Email/SMS
    - **API** : Couche FastAPI avec validation Pydantic
    """,
    version="1.0.0",
    contact={
        "name": "Équipe Développement SONAMINES",
        "email": "dev@sonamines.com",
    },
    lifespan=lifespan,
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Gestionnaires d'exceptions globaux
@app.exception_handler(DomainException)
async def domain_exception_handler(request: Request, exc: DomainException):
    """Gestionnaire pour les exceptions du domaine métier."""
    logger.warning(
        "Erreur domaine métier",
        exception_type=type(exc).__name__,
        message=str(exc),
        path=request.url.path,
    )
    
    # Mapping des exceptions domaine vers codes HTTP
    status_code_mapping = {
        UtilisateurExistantError: status.HTTP_409_CONFLICT,
        UtilisateurIntrouvableError: status.HTTP_404_NOT_FOUND,
        OffreIntrouvableError: status.HTTP_404_NOT_FOUND,
        CandidatureIntrouvableError: status.HTTP_404_NOT_FOUND,
        AuthentificationEchoueeError: status.HTTP_401_UNAUTHORIZED,
        AutorisationRefuseeError: status.HTTP_403_FORBIDDEN,
        CanalNonVerifieError: status.HTTP_400_BAD_REQUEST,
        CandidatureNonEligibleError: status.HTTP_400_BAD_REQUEST,
        OffreClotureeError: status.HTTP_400_BAD_REQUEST,
        StatutCandidatureInvalideError: status.HTTP_400_BAD_REQUEST,
        FichierTropVolumineuxError: status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
        FormatFichierNonSupporteError: status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    }
    
    status_code = status_code_mapping.get(type(exc), status.HTTP_400_BAD_REQUEST)
    
    return JSONResponse(
        status_code=status_code,
        content={
            "error": type(exc).__name__,
            "message": str(exc),
            "details": getattr(exc, "__dict__", {}),
        },
    )


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Gestionnaire pour les erreurs de validation."""
    logger.warning(
        "Erreur de validation",
        message=str(exc),
        path=request.url.path,
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "ValidationError",
            "message": str(exc),
        },
    )


@app.exception_handler(500)
async def internal_server_error_handler(request: Request, exc: Exception):
    """Gestionnaire pour les erreurs internes."""
    logger.error(
        "Erreur interne du serveur",
        exception_type=type(exc).__name__,
        message=str(exc),
        path=request.url.path,
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "InternalServerError",
            "message": "Une erreur interne s'est produite",
        },
    )


# Montage des routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(moi_router, prefix="/api/v1")
app.include_router(candidats_router, prefix="/api/v1")
app.include_router(offres_router, prefix="/api/v1")
app.include_router(candidatures_router, prefix="/api/v1")
app.include_router(notifications_router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/v1")


# Route de santé
@app.get(
    "/health",
    tags=["Santé"],
    summary="Vérification de santé",
    description="Vérifie que l'API est opérationnelle",
)
async def health_check():
    """Point de contrôle de santé de l'API."""
    return {
        "status": "healthy",
        "service": "SONAMINES Candidatures API",
        "version": "1.0.0",
        "environment": "development",  # À adapter selon l'environnement
    }


# Route racine
@app.get(
    "/",
    tags=["Informations"],
    summary="Informations sur l'API",
    description="Retourne les informations générales sur l'API",
)
async def root():
    """Informations sur l'API."""
    return {
        "message": "Bienvenue sur l'API SONAMINES - Plateforme de Candidatures",
        "version": "1.0.0",
        "documentation": "/docs",
        "redoc": "/redoc",
        "health": "/health",
    }