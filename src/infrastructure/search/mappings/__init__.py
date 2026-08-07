"""Mappings Elasticsearch pour l'indexation."""

from .candidature_mapping import CANDIDATURE_MAPPING
from .offre_mapping import OFFRE_MAPPING

__all__ = [
    "CANDIDATURE_MAPPING",
    "OFFRE_MAPPING",
]