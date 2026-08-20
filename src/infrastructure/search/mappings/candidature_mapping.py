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
        },
        # Champs du profil candidat dénormalisés pour la recherche multicritère
        "candidat_sexe": {
            "type": "keyword"
        },
        "candidat_date_naissance": {
            "type": "date",
            "format": "strict_date_optional_time||epoch_millis"
        },
        "candidat_nationalite": {
            "type": "keyword"
        },
        "candidat_region_origine": {
            "type": "keyword"
        },
        "candidat_region_residence": {
            "type": "keyword"
        },
        "candidat_langues_parlees": {
            "type": "keyword"
        },
        "candidat_disponibilite": {
            "type": "keyword"
        },
        "candidat_niveau_academique": {
            "type": "keyword"
        },
        "candidat_domaine_formation": {
            "type": "keyword"
        },
        "candidat_specialite": {
            "type": "keyword"
        },
        "candidat_competences": {
            "type": "keyword"
        },
        # Caractéristiques de l'offre associée (pour filtrer emploi/stage)
        "offre_type_offre": {
            "type": "keyword"
        },
        "offre_type_stage": {
            "type": "keyword"
        }
    }
}