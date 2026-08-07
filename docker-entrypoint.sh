#!/bin/bash
# Script d'entrée Docker pour SONAMINES Candidatures
# Gère les migrations, l'initialisation et le démarrage de l'application

set -e

# Couleurs pour les logs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Démarrage de SONAMINES Candidatures${NC}"
echo "======================================================="

# Fonction utilitaire de test de port avec /dev/tcp
test_tcp_connection() {
    local host=$1
    local port=$2
    (echo > /dev/tcp/$host/$port) 2>/dev/null
}

# Fonction d'attente pour les services externes
wait_for_service() {
    local host=$1
    local port=$2
    local service=$3
    local max_attempts=30
    local attempt=1

    echo -e "${YELLOW}⏳ Attente du service $service ($host:$port)...${NC}"
    
    while ! test_tcp_connection "$host" "$port"; do
        if [ $attempt -eq $max_attempts ]; then
            echo -e "${RED}❌ Impossible de se connecter à $service après $max_attempts tentatives${NC}"
            echo -e "${RED}   Vérifiez que le service est démarré et accessible sur $host:$port${NC}"
            exit 1
        fi
        echo -e "${YELLOW}   Tentative $attempt/$max_attempts...${NC}"
        sleep 2
        ((attempt++))
    done
    
    echo -e "${GREEN}✅ Service $service disponible${NC}"
}

# Fonction de test de connexion base de données
test_database() {
    echo -e "${YELLOW}🔍 Test de connexion à la base de données...${NC}"
    
    if python3 -c "
import asyncio
import sys
sys.path.append('.')
from src.infrastructure.config import settings
from test_db_connection import test_db_connection

async def main():
    try:
        return await test_db_connection()
    except Exception as e:
        print(f'Erreur: {e}')
        return False

result = asyncio.run(main())
sys.exit(0 if result else 1)
"; then
        echo -e "${GREEN}✅ Connexion base de données OK${NC}"
        return 0
    else
        echo -e "${RED}❌ Échec de connexion base de données${NC}"
        return 1
    fi
}

# Fonction de migration base de données
run_migrations() {
    echo -e "${YELLOW}📦 Exécution des migrations Alembic...${NC}"
    
    # Upgrade vers la dernière version
    if alembic upgrade head; then
        echo -e "${GREEN}✅ Migrations appliquées avec succès${NC}"
        return 0
    else
        echo -e "${RED}❌ Échec des migrations${NC}"
        return 1
    fi
}

# Fonction de vérification de santé des services externes
check_external_services() {
    # PostgreSQL
    if [ -n "$DATABASE_URL" ]; then
        DB_HOST=$(echo $DATABASE_URL | sed -n 's/.*@\([^:]*\):.*/\1/p')
        DB_PORT=$(echo $DATABASE_URL | sed -n 's/.*:\([0-9]*\)\/.*/\1/p')
        if [ -n "$DB_HOST" ] && [ -n "$DB_PORT" ]; then
            wait_for_service "$DB_HOST" "$DB_PORT" "PostgreSQL"
        fi
    fi
    
    # Elasticsearch (optionnel)
    if [ -n "$ELASTICSEARCH_URL" ]; then
        ES_HOST=$(echo $ELASTICSEARCH_URL | sed 's|http://||' | cut -d':' -f1)
        ES_PORT=$(echo $ELASTICSEARCH_URL | sed 's|http://||' | cut -d':' -f2)
        ES_PORT=${ES_PORT:-9200}
        echo -e "${YELLOW}⏳ Test optionnel d'Elasticsearch...${NC}"
        if wait_for_service "$ES_HOST" "$ES_PORT" "Elasticsearch" 2>/dev/null; then
            echo -e "${GREEN}✅ Elasticsearch disponible${NC}"
        else
            echo -e "${YELLOW}⚠️  Elasticsearch non disponible (optionnel)${NC}"
        fi
    fi
    
    # MinIO (optionnel)
    if [ -n "$MINIO_ENDPOINT" ]; then
        MINIO_HOST=$(echo $MINIO_ENDPOINT | cut -d':' -f1)
        MINIO_PORT=$(echo $MINIO_ENDPOINT | cut -d':' -f2)
        MINIO_PORT=${MINIO_PORT:-9000}
        echo -e "${YELLOW}⏳ Test optionnel de MinIO...${NC}"
        if wait_for_service "$MINIO_HOST" "$MINIO_PORT" "MinIO" 2>/dev/null; then
            echo -e "${GREEN}✅ MinIO disponible${NC}"
        else
            echo -e "${YELLOW}⚠️  MinIO non disponible (optionnel)${NC}"
        fi
    fi
}

# Mode de démarrage selon les arguments
case "${1:-start}" in
    "migrate")
        echo -e "${BLUE}🔧 Mode: Migration uniquement${NC}"
        check_external_services
        test_database && run_migrations
        ;;
    "test")
        echo -e "${BLUE}🧪 Mode: Tests${NC}"
        check_external_services
        test_database
        echo -e "${GREEN}✅ Tests de santé terminés${NC}"
        ;;
    "dev"|"development")
        echo -e "${BLUE}🛠️  Mode: Développement${NC}"
        check_external_services
        test_database && run_migrations
        echo -e "${GREEN}🚀 Démarrage en mode développement...${NC}"
        exec uvicorn src.api.main:app --host 0.0.0.0 --port "${PORT:-8000}" --reload --log-level debug
        ;;
    "prod"|"production")
        echo -e "${BLUE}🏭 Mode: Production${NC}"
        check_external_services
        test_database && run_migrations
        echo -e "${GREEN}🚀 Démarrage en mode production...${NC}"
        exec uvicorn src.api.main:app --host 0.0.0.0 --port "${PORT:-8000}" --workers "${WORKERS:-4}" --log-level info
        ;;
    "start"|*)
        echo -e "${BLUE}🚀 Mode: Démarrage standard${NC}"
        check_external_services
        
        # Tentative de migration automatique
        if test_database; then
            echo -e "${YELLOW}📦 Tentative de migration automatique...${NC}"
            run_migrations || echo -e "${YELLOW}⚠️  Migration échouée, continue quand même...${NC}"
        fi
        
        echo -e "${GREEN}🚀 Démarrage de l'application...${NC}"
        exec "$@"
        ;;
esac

echo -e "${GREEN}✅ Script d'entrée terminé${NC}"