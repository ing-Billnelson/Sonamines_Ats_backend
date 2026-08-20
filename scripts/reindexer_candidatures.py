"""Script one-shot : recrée l'index candidatures et réindexe tout depuis PostgreSQL.

Usage (dans un conteneur avec le code et l'accès réseau db/elasticsearch) :
    python -m scripts.reindexer_candidatures
"""

import asyncio

from src.infrastructure.config import settings
from src.infrastructure.db.session import async_session_factory
from src.infrastructure.db.repositories.postgres_candidature_repository import (
    PostgresCandidatureRepository,
)
from src.infrastructure.db.repositories.postgres_offre_repository import (
    PostgresOffreRepository,
)
from src.infrastructure.db.repositories.postgres_utilisateur_repository import (
    PostgresUtilisateurRepository,
)
from src.infrastructure.search.elasticsearch_adapter import ElasticsearchAdapter


async def main() -> None:
    search_port = ElasticsearchAdapter(settings)

    # 1. Recrée l'index candidatures proprement avec CANDIDATURE_MAPPING
    reinitialise = await search_port.reinitialiser_index_candidatures()
    if not reinitialise:
        raise RuntimeError("Impossible de recréer l'index candidatures")
    print("Index 'candidatures' recréé avec le mapping CANDIDATURE_MAPPING")

    async with async_session_factory() as session:
        candidature_repository = PostgresCandidatureRepository(session)
        utilisateur_repository = PostgresUtilisateurRepository(session)
        offre_repository = PostgresOffreRepository(session)

        # 2. Récupère toutes les candidatures existantes (sans filtre, paginé)
        candidatures, total = await candidature_repository.lister_toutes(
            page=1, taille_page=100000
        )
        print(f"{total} candidature(s) trouvée(s) en base")

        # 3. Réindexe chaque candidature avec les infos candidat et offre
        nb_indexees = 0
        nb_echouees = 0
        for candidature in candidatures:
            candidat = await utilisateur_repository.obtenir_candidat_par_id(
                candidature.candidat_id
            )
            offre = None
            if candidature.offre_id is not None:
                offre = await offre_repository.obtenir_par_id(candidature.offre_id)

            ok = await search_port.indexer_candidature(
                candidature, candidat=candidat, offre=offre
            )
            if ok:
                nb_indexees += 1
            else:
                nb_echouees += 1
                print(f"  [ÉCHEC] candidature {candidature.id}")

        print(f"Réindexées : {nb_indexees} | Échecs : {nb_echouees}")


if __name__ == "__main__":
    asyncio.run(main())
