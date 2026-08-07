"""Routers de l'API v1."""

from .admin import router as admin_router
from .auth import router as auth_router
from .candidats import router as candidats_router
from .candidatures import router as candidatures_router
from .moi import router as moi_router
from .notifications import router as notifications_router
from .offres import router as offres_router

__all__ = [
    "admin_router",
    "auth_router",
    "candidats_router",
    "candidatures_router",
    "moi_router",
    "notifications_router",
    "offres_router",
]