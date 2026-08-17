"""Mapping Elasticsearch pour les offres."""

# Mapping détaillé pour l'indexation des offres
OFFRE_MAPPING = {
    "properties": {
        "id": {
            "type": "keyword"
        },
        "numero_reference": {
            "type": "keyword"
        },
        "titre": {
            "type": "text",
            "analyzer": "french",
            "fields": {
                "keyword": {
                    "type": "keyword"
                }
            }
        },
        "description": {
            "type": "text",
            "analyzer": "french"
        },
        "type_offre": {
            "type": "keyword"
        },
        "type_contrat": {
            "type": "keyword"
        },
        "type_stage": {
            "type": "keyword"
        },
        "statut": {
            "type": "keyword"
        },
        "lieu": {
            "type": "text",
            "analyzer": "french",
            "fields": {
                "keyword": {
                    "type": "keyword"
                }
            }
        },
        "salaire_min": {
            "type": "float"
        },
        "salaire_max": {
            "type": "float"
        },
        "competences_requises": {
            "type": "keyword"
        },
        "experience_requise": {
            "type": "text",
            "analyzer": "french"
        },
        "date_creation": {
            "type": "date",
            "format": "strict_date_optional_time||epoch_millis"
        },
        "date_publication": {
            "type": "date",
            "format": "strict_date_optional_time||epoch_millis"
        },
        "date_limite_candidature": {
            "type": "date",
            "format": "strict_date_optional_time||epoch_millis"
        },
        "date_cloture": {
            "type": "date",
            "format": "strict_date_optional_time||epoch_millis"
        },
        "suggest_titre": {
            "type": "completion",
            "analyzer": "standard"
        }
    }
}