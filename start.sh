#!/bin/bash
# Script de démarrage rapide pour SONAMINES Candidatures
# Usage: ./start.sh [dev|prod|test|stop|logs]

set -e

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="sonamines-candidatures"
COMPOSE_FILE="docker-compose.yml"

# Fonctions utilitaires
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Vérification des prérequis
check_requirements() {
    log_info "Vérification des prérequis..."
    
    if ! command -v docker &> /dev/null; then
        log_error "Docker n'est pas installé"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null && ! command -v docker compose &> /dev/null; then
        log_error "Docker Compose n'est pas installé"
        exit 1
    fi
    
    # Utiliser docker compose ou docker-compose selon ce qui est disponible
    if command -v docker compose &> /dev/null; then
        COMPOSE_CMD="docker compose"
    else
        COMPOSE_CMD="docker-compose"
    fi
    
    log_success "Prérequis OK"
}

# Création des répertoires nécessaires
create_directories() {
    log_info "Création des répertoires nécessaires..."
    mkdir -p uploads logs init-scripts
    log_success "Répertoires créés"
}

# Configuration environnement
setup_env() {
    if [ ! -f .env ]; then
        log_info "Création du fichier .env depuis .env.example..."
        if [ -f .env.example ]; then
            cp .env.example .env
        else
            log_warning "Fichier .env.example introuvable, création d'un .env basique"
            cat > .env << 'EOF'
# Configuration de développement
DATABASE_URL=postgresql+asyncpg://sonamines:sonamines123@localhost:5432/sonamines_candidatures
ELASTICSEARCH_URL=http://localhost:9200
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=admin
MINIO_SECRET_KEY=admin123
JWT_SECRET_KEY=dev-jwt-secret-key-change-in-production
MAX_TAILLE_DOCUMENT_MO=10
MAX_TAILLE_PHOTO_MO=2
FORMATS_DOCUMENTS_AUTORISES=pdf,doc,docx,jpg,jpeg,png
FORMATS_PHOTO_AUTORISES=jpg,jpeg,png
LOG_LEVEL=INFO
EOF
        fi
        log_success "Fichier .env créé"
    else
        log_info "Fichier .env existant"
    fi
}

# Démarrage en mode développement
start_dev() {
    log_info "🚀 Démarrage en mode développement..."
    
    create_directories
    setup_env
    
    # Démarrage des services infrastructure d'abord
    log_info "Démarrage des services infrastructure..."
    $COMPOSE_CMD up -d db elasticsearch minio redis
    
    # Attendre que les services soient prêts
    log_info "Attente de la disponibilité des services..."
    sleep 10
    
    # Vérification de santé
    log_info "Vérification de la santé des services..."
    timeout 60 bash -c 'until docker exec sonamines-candidatures-db pg_isready -U sonamines -d sonamines_candidatures; do sleep 2; done'
    log_success "PostgreSQL prêt"
    
    timeout 60 bash -c 'until curl -s http://localhost:9200/_cluster/health; do sleep 2; done'
    log_success "Elasticsearch prêt"
    
    timeout 60 bash -c 'until curl -s http://localhost:9000/minio/health/live; do sleep 2; done'
    log_success "MinIO prêt"
    
    # Migrations de base de données
    log_info "Exécution des migrations..."
    python3 -m alembic upgrade head || log_warning "Migrations échouées, continuez manuellement"
    
    # Démarrage de l'application
    log_info "Démarrage de l'application FastAPI..."
    $COMPOSE_CMD up -d app
    
    log_success "🎉 Application démarrée en mode développement!"
    echo ""
    echo "📋 Services disponibles:"
    echo "  🌐 API: http://localhost:8000"
    echo "  📖 Documentation: http://localhost:8000/docs"
    echo "  🗄️  Base de données: localhost:5432"
    echo "  🔍 Elasticsearch: http://localhost:9200"
    echo "  📁 MinIO: http://localhost:9001 (admin/admin123)"
    echo "  💾 Redis: localhost:6379"
    echo ""
    echo "📊 Services optionnels (--profile admin):"
    echo "  🔧 PgAdmin: http://localhost:8080"
    echo "  📈 Kibana: http://localhost:5601"
    echo ""
    echo "📝 Commandes utiles:"
    echo "  ./start.sh logs     # Voir les logs"
    echo "  ./start.sh stop     # Arrêter les services"
    echo "  ./start.sh test     # Tests de santé"
}

# Démarrage en mode production
start_prod() {
    log_info "🏭 Démarrage en mode production..."
    
    create_directories
    setup_env
    
    # Build et démarrage
    $COMPOSE_CMD up -d --build
    
    log_success "🚀 Application démarrée en mode production!"
    echo ""
    echo "📋 Services disponibles:"
    echo "  🌐 API: http://localhost:8000"
    echo "  📖 Documentation: http://localhost:8000/docs"
}

# Tests de santé
run_tests() {
    log_info "🧪 Exécution des tests de santé..."
    
    # Test de l'API
    if curl -f -s http://localhost:8000/health > /dev/null; then
        log_success "✅ API accessible"
    else
        log_error "❌ API inaccessible"
    fi
    
    # Test base de données
    if docker exec sonamines-candidatures-db pg_isready -U sonamines -d sonamines_candidatures > /dev/null 2>&1; then
        log_success "✅ PostgreSQL accessible"
    else
        log_error "❌ PostgreSQL inaccessible"
    fi
    
    # Test Elasticsearch
    if curl -f -s http://localhost:9200/_cluster/health > /dev/null; then
        log_success "✅ Elasticsearch accessible"
    else
        log_error "❌ Elasticsearch inaccessible"
    fi
    
    # Test MinIO
    if curl -f -s http://localhost:9000/minio/health/live > /dev/null; then
        log_success "✅ MinIO accessible"
    else
        log_error "❌ MinIO inaccessible"
    fi
    
    # Test Redis
    if docker exec sonamines-candidatures-redis redis-cli ping > /dev/null 2>&1; then
        log_success "✅ Redis accessible"
    else
        log_error "❌ Redis inaccessible"
    fi
    
    log_info "Tests terminés"
}

# Affichage des logs
show_logs() {
    log_info "📝 Affichage des logs (Ctrl+C pour quitter)..."
    $COMPOSE_CMD logs -f
}

# Arrêt des services
stop_services() {
    log_info "🛑 Arrêt des services..."
    $COMPOSE_CMD down
    log_success "Services arrêtés"
}

# Nettoyage complet
clean_all() {
    log_warning "🧹 Nettoyage complet (suppression des volumes)..."
    read -p "Êtes-vous sûr ? Cela supprimera toutes les données (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        $COMPOSE_CMD down -v --remove-orphans
        docker system prune -f
        log_success "Nettoyage terminé"
    else
        log_info "Nettoyage annulé"
    fi
}

# Affichage de l'aide
show_help() {
    cat << 'EOF'
🏢 SONAMINES Candidatures - Script de démarrage

Usage: ./start.sh [COMMAND]

Commands:
  dev       Démarrer en mode développement (par défaut)
  prod      Démarrer en mode production
  stop      Arrêter tous les services
  logs      Afficher les logs en temps réel
  test      Exécuter les tests de santé
  clean     Nettoyage complet (supprime les données)
  help      Afficher cette aide

Examples:
  ./start.sh            # Démarrage développement
  ./start.sh dev        # Démarrage développement 
  ./start.sh prod       # Démarrage production
  ./start.sh logs       # Voir les logs
  ./start.sh test       # Tests de santé
  ./start.sh stop       # Arrêt des services

Profils Docker Compose optionnels:
  --profile admin       # Ajouter PgAdmin et Kibana
  --profile monitoring  # Ajouter Kibana seulement

Environment:
  Copier .env.example vers .env et adapter selon votre environnement

Documentation complète: voir README.md
EOF
}

# Script principal
main() {
    check_requirements
    
    case "${1:-dev}" in
        "dev"|"development")
            start_dev
            ;;
        "prod"|"production")
            start_prod
            ;;
        "test"|"health")
            run_tests
            ;;
        "logs")
            show_logs
            ;;
        "stop")
            stop_services
            ;;
        "clean")
            clean_all
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            log_error "Commande inconnue: $1"
            show_help
            exit 1
            ;;
    esac
}

# Exécution du script
main "$@"