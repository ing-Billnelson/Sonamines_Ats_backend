"""Configuration de la session de base de données SQLAlchemy async."""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ...infrastructure.config import settings

# Configuration de l'engine async SQLAlchemy
engine = create_async_engine(
    settings.database_url,
    echo=False,  # Mettre à True pour debug SQL
    pool_size=5,  # Nombre de connexions dans le pool
    max_overflow=10,  # Connexions supplémentaires autorisées
    pool_pre_ping=True,  # Vérification de la connexion avant utilisation
    pool_recycle=3600,  # Recyclage des connexions après 1h
)

# Configuration du sessionmaker async
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Évite les erreurs après commit
    autoflush=True,  # Flush automatique avant les requêtes
    autocommit=False,  # Pas d'autocommit, gestion manuelle des transactions
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Générateur de session de base de données pour l'injection de dépendances FastAPI.
    
    Usage:
        @app.get("/users/")
        async def get_users(db: AsyncSession = Depends(get_db)):
            # Utiliser db ici
            pass
    
    Yields:
        AsyncSession: Session de base de données configurée
        
    Note:
        La session est automatiquement fermée après utilisation,
        même en cas d'exception.
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            # En cas d'erreur, on rollback la transaction
            await session.rollback()
            raise
        finally:
            # La session est automatiquement fermée grâce au context manager
            await session.close()