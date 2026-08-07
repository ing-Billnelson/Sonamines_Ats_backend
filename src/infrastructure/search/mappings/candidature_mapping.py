"""Mapping Elasticsearch pour les candidatures."""

# Mapping détaillé pour l'indexation des candidatures
CANDIDATURE_MAPPING = {
    "properties": {
        "id": {
            "type": "keyword"
        },
        "numero_reference": {
            "type": "keyword"
        },
        "candidat_id": {
            "type": "keyword"
        },
        "offre_id": {
            "type": "keyword"
        },
        "statut": {
            "type": "keyword"
        },
        "message_motivation": {
            "type": "text",
            "analyzer": "standard"
        },
        "notes_internes": {
            "type": "text",
            "analyzer": "standard"
        },
        "date_soumission": {
            "type": "date",
            "format": "strict_date_optional_time||epoch_millis"
        },
        "date_derniere_modification": {
            "type": "date",
            "format": "strict_date_optional_time||epoch_millis"
        },
        "est_spontanee": {
            "type": "boolean"
        },
        # Champs dénormalisés pour faciliter les recherches
        "candidat_nom": {
            "type": "text",
            "analyzer": "standard",
            "fields": {
                "keyword": {
                    "type": "keyword"
                }
            }
        },
        "candidat_prenom": {
            "type": "text",
            "analyzer": "standard",
            "fields": {
                "keyword": {
                    "type": "keyword"
                }
            }
        },
        "candidat_email": {
            "type": "keyword"
        },
        "offre_titre": {
            "type": "text",
            "analyzer": "standard"
        },
        "offre_lieu": {
            "type": "keyword"
        }
    }
}