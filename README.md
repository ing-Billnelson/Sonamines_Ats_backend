# 🏢 SONAMINES - Plateforme de Candidatures

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://www.postgresql.org)
[![Architecture](https://img.shields.io/badge/Architecture-Hexagonale-orange.svg)](https://alistair.cockburn.us/hexagonal-architecture/)

> Plateforme moderne de gestion des candidatures pour SONAMINES, construite avec une architecture hexagonale (ports & adapters) garantissant la maintenabilité, testabilité et évolutivité.

## 📋 Table des matières

- [🎯 Vue d'ensemble](#-vue-densemble)
- [🏗️ Architecture](#️-architecture)
- [🚀 Installation rapide](#-installation-rapide)
- [📖 Guide de développement](#-guide-de-développement)
- [🔧 Configuration](#-configuration)
- [📊 Base de données](#-base-de-données)
- [🧪 Tests](#-tests)
- [📦 Déploiement](#-déploiement)
- [🤝 Contribution](#-contribution)

## 🎯 Vue d'ensemble

La plateforme SONAMINES Candidatures est une solution complète de gestion des candidatures d'emploi, implémentant les meilleures pratiques du développement logiciel :

### ✨ Fonctionnalités principales

- **👤 Gestion des candidats** : Inscription, authentification, profils complets
- **👨‍💼 Administration RH** : Gestion des offres, évaluation des candidatures
- **📄 Gestion documentaire** : Upload sécurisé avec validation (CV, lettres, certifications)
- **📧 Notifications duales** : Système de notification interne + externe (email/SMS)
- **🔍 Recherche avancée** : Recherche full-text avec Elasticsearch
- **📊 Suivi complet** : Historique détaillé des changements de statut

### 🎯 Règles métier strictes

1. **Notification duale obligatoire** : Chaque action génère une notification interne ET un envoi externe exclusif (email OU SMS selon canal_validation)
2. **Fichiers différenciés** : DOCUMENT (10Mo max, pdf/doc/docx/jpg/jpeg/png) vs PHOTO (2Mo max, jpg/jpeg/png uniquement)
3. **Validation multi-canal** : Email ou téléphone selon préférence utilisateur
4. **Audit trail complet** : Traçabilité complète de tous les changements

## 🏗️ Architecture

### Architecture hexagonale (Ports & Adapters)

```
src/
├── domain/           # 🎯 Cœur métier (indépendant)
│   ├── entities/     # Entités métier
│   ├── enums/        # Énumérations métier  
│   ├── exceptions/   # Exceptions métier
│   ├── ports/        # Interfaces (contrats)
│   └── value_objects/ # Objets valeur
├── application/      # 🔄 Cas d'usage
│   ├── dto/          # Data Transfer Objects
│   └── use_cases/    # Logique applicative
├── infrastructure/   # 🔌 Adapters techniques
│   ├── adapters/     # Implémentations concrètes
│   ├── config/       # Configuration
│   └── db/          # Base de données
└── api/             # 🌐 Interface REST
    ├── routers/      # Routes FastAPI
    ├── schemas/      # Schemas Pydantic
    └── dependencies/ # Injection de dépendances
```

### 🎨 Principes de conception

- **🔒 Inversion de dépendance** : Le domaine ne dépend d'aucun framework
- **🔌 Ports & Adapters** : Interfaces claires entre couches
- **🧪 Testabilité** : Mocking facile grâce aux abstractions
- **📦 Single Responsibility** : Une responsabilité par classe/module
- **🔄 CQRS** : Séparation lecture/écriture pour les cas complexes

### 🛠️ Stack technique

| Composant | Technologie | Version | Rôle |
|-----------|-------------|---------|------|
| **Backend** | FastAPI | 0.104+ | API REST moderne et performante |
| **Base de données** | PostgreSQL | 15+ | Stockage relationnel ACID |
| **Recherche** | Elasticsearch | 8.x | Recherche full-text avancée |
| **Stockage fichiers** | MinIO | RELEASE.2023+ | Stockage S3-compatible |
| **ORM** | SQLAlchemy | 2.0+ | Mapping objet-relationnel async |
| **Migrations** | Alembic | 1.13+ | Gestion des migrations DB |
| **Validation** | Pydantic | 2.7+ | Validation et sérialisation |
| **Tests** | Pytest | 7.4+ | Framework de tests |
| **Qualité** | MyPy, Black, isort | - | Typage, formatage, imports |

## 🚀 Installation rapide

### Prérequis

- **Python 3.11+**
- **PostgreSQL 15+** 
- **Docker & Docker Compose** (optionnel)
- **Git**

### 🐳 Avec Docker (recommandé)

```bash
# 1. Cloner le projet
git clone <repository-url>
cd sonamines-candidatures

# 2. Configuration
cp .env.example .env
# Éditer .env selon votre environnement

# 3. Démarrage avec Docker Compose
docker-compose up -d

# 4. Vérifier le démarrage
curl http://localhost:8000/health
```

### 🐍 Installation locale

```bash
# 1. Cloner et configurer
git clone <repository-url>
cd sonamines-candidatures
cp .env.example .env

# 2. Environnement virtuel Python
python3.11 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows

# 3. Installation des dépendances
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4. Configuration de la base de données
# Créer la base PostgreSQL
createdb sonamines_candidatures

# 5. Migrations
alembic upgrade head

# 6. Lancer l'application
uvicorn src.api.main:app --reload
```

### 🧪 Test de l'installation

```bash
# Test de connectivité
python test_db_connection.py

# Tests unitaires
pytest

# Vérification API
curl http://localhost:8000/docs
```

## 📖 Guide de développement

### 🔄 Workflow de développement

```bash
# 1. Créer une branche feature
git checkout -b feature/nouvelle-fonctionnalite

# 2. Développer en suivant l'architecture hexagonale
# - Commencer par le domaine (entities, value objects)
# - Créer les ports (interfaces)
# - Implémenter les use cases
# - Créer les adapters (infrastructure) 
# - Exposer via l'API

# 3. Tests automatisés
pytest tests/

# 4. Vérifications qualité
mypy src/
black src/ tests/
isort src/ tests/

# 5. Migration si nécessaire
alembic revision --autogenerate -m "Description du changement"
alembic upgrade head
```

### 🎯 Règles de développement

#### ✅ DO (À faire)

- **Respecter l'architecture hexagonale** : Domaine → Application → Infrastructure → API
- **Types strictes** : Utiliser mypy et les annotations de types
- **Tests en TDD** : Tests avant implémentation
- **Docstrings complètes** : Documentation de toutes les fonctions publiques
- **Gestion des erreurs** : Exceptions métier explicites
- **Logs structurés** : Utilisation du logging Python

#### ❌ DON'T (À éviter)

- **Imports circulaires** : Vérifier les dépendances
- **Logique métier dans l'API** : Garder les routers simples
- **Dépendances frameworks dans le domaine** : Indépendance stricte
- **Magic numbers** : Utiliser des constantes nommées
- **Commits sans tests** : Couverture obligatoire

### 🧩 Ajout d'une nouvelle fonctionnalité

#### Exemple : Ajouter un système de favoris

```bash
# 1. Domaine
touch src/domain/entities/favori.py
touch src/domain/ports/favori_repository.py

# 2. Application  
touch src/application/use_cases/ajouter_favori_use_case.py
touch src/application/dto/favori_dto.py

# 3. Infrastructure
touch src/infrastructure/db/models/favori_model.py
touch src/infrastructure/adapters/repositories/favori_repository.py

# 4. API
touch src/api/routers/favoris.py
touch src/api/schemas/favori_schema.py

# 5. Tests
touch tests/domain/entities/test_favori.py
touch tests/application/use_cases/test_ajouter_favori.py
# etc.

# 6. Migration
alembic revision --autogenerate -m "Ajout système favoris"
```

## 🔧 Configuration

### Variables d'environnement

```bash
# Base de données
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/sonamines

# Elasticsearch (optionnel)
ELASTICSEARCH_URL=http://localhost:9200

# MinIO (optionnel)
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=admin
MINIO_SECRET_KEY=admin123

# JWT
JWT_SECRET_KEY=your-super-secret-jwt-key-here
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# Contraintes fichiers
MAX_TAILLE_DOCUMENT_MO=10
MAX_TAILLE_PHOTO_MO=2
FORMATS_DOCUMENTS_AUTORISES=pdf,doc,docx,jpg,jpeg,png
FORMATS_PHOTO_AUTORISES=jpg,jpeg,png

# SMTP (email)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=votre-email@sonamines.com
SMTP_PASSWORD=votre-mot-de-passe
SMTP_TLS=true

# SMS
SMS_API_KEY=votre-cle-api-sms
SMS_API_URL=https://api.sms-provider.com

# Logs
LOG_LEVEL=INFO
```

### 🗄️ Base de données

#### Structure des tables

- **`utilisateurs`** : Candidats et administrateurs RH (polymorphisme)
- **`offres`** : Offres d'emploi avec statuts et métadonnées
- **`candidatures`** : Candidatures avec statut et documents liés
- **`documents`** : Fichiers uploadés (CV, lettres, etc.)
- **`historique_statuts`** : Audit trail des changements
- **`notifications`** : Notifications internes et externes

#### Relations principales

```sql
utilisateurs (1) ←→ (N) candidatures
offres (1) ←→ (N) candidatures  
candidatures (1) ←→ (N) documents
candidatures (1) ←→ (N) historique_statuts
utilisateurs (1) ←→ (N) notifications
```

#### Indexes performants

```sql
-- Performance des requêtes fréquentes
CREATE INDEX ix_candidatures_candidat_offre_unique ON candidatures(candidat_id, offre_id);
CREATE INDEX ix_notifications_utilisateur_lue ON notifications(utilisateur_id, lue);
CREATE INDEX ix_documents_candidature_type ON documents(candidature_id, type_document);
```

### 🔍 Elasticsearch (optionnel)

Configuration pour la recherche full-text :

```json
{
  "mappings": {
    "properties": {
      "titre": {"type": "text", "analyzer": "french"},
      "description": {"type": "text", "analyzer": "french"},
      "competences": {"type": "keyword"},
      "lieu": {"type": "keyword"},
      "departement": {"type": "keyword"}
    }
  }
}
```

## 🧪 Tests

### Structure des tests

```
tests/
├── unit/                # Tests unitaires
│   ├── domain/         # Tests du domaine
│   ├── application/    # Tests des use cases
│   └── infrastructure/ # Tests des adapters
├── integration/        # Tests d'intégration
├── e2e/               # Tests end-to-end
└── fixtures/          # Données de test
```

### Commandes de test

```bash
# Tests complets
pytest

# Tests avec couverture
pytest --cov=src --cov-report=html

# Tests unitaires uniquement
pytest tests/unit/

# Tests d'un module spécifique
pytest tests/unit/domain/entities/test_candidat.py

# Tests en mode watch (développement)
pytest-watch

# Performance et profiling
pytest --benchmark-only
```

### 🎯 Stratégie de test

1. **Tests unitaires** : Chaque classe métier, use case isolé
2. **Tests d'intégration** : Repositories avec DB réelle
3. **Tests API** : Endpoints avec TestClient FastAPI
4. **Tests E2E** : Scénarios utilisateur complets

### Exemple de test

```python
# tests/unit/domain/entities/test_candidat.py
import pytest
from src.domain.entities.candidat import Candidat
from src.domain.value_objects.email import Email

def test_candidat_creation_valide():
    # Given
    email = Email("test@sonamines.com")
    
    # When
    candidat = Candidat.creer_nouveau(
        email=email,
        mot_de_passe_hash="hash123",
        nom="Doe",
        prenom="John"
    )
    
    # Then
    assert candidat.email == email
    assert candidat.statut == StatutCompte.EN_ATTENTE_VALIDATION
    assert not candidat.email_verifie
```

## 📦 Déploiement

### 🐳 Docker Production

```bash
# Build l'image de production
docker build -t sonamines/candidatures:latest .

# Démarrage en production
docker run -d \
  --name sonamines-candidatures \
  -p 8000:8000 \
  -e DATABASE_URL="postgresql+asyncpg://..." \
  -e JWT_SECRET_KEY="production-secret" \
  --restart unless-stopped \
  sonamines/candidatures:latest prod
```

### ☸️ Kubernetes

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sonamines-candidatures
spec:
  replicas: 3
  selector:
    matchLabels:
      app: sonamines-candidatures
  template:
    metadata:
      labels:
        app: sonamines-candidatures
    spec:
      containers:
      - name: app
        image: sonamines/candidatures:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        - name: JWT_SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: jwt-secret
              key: key
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### 🔄 CI/CD Pipeline

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run tests
      run: |
        pytest --cov=src --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
  
  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Build and push Docker image
      run: |
        docker build -t sonamines/candidatures:${{ github.sha }} .
        docker push sonamines/candidatures:${{ github.sha }}
    
    - name: Deploy to production
      run: |
        # Commandes de déploiement K8s/Cloud
        kubectl set image deployment/sonamines-candidatures app=sonamines/candidatures:${{ github.sha }}
```

## 🔒 Sécurité

### Mesures implémentées

- **🔐 Authentification JWT** : Tokens sécurisés avec expiration
- **🛡️ Validation stricte** : Pydantic sur toutes les entrées
- **🚫 SQL Injection** : SQLAlchemy ORM + requêtes préparées
- **📁 Upload sécurisé** : Validation type MIME + taille + antivirus
- **🌐 CORS configuré** : Origines autorisées uniquement
- **📝 Logs d'audit** : Traçabilité complète des actions
- **🔒 Secrets externes** : Variables d'environnement chiffrées

### Checklist sécurité production

- [ ] JWT_SECRET_KEY cryptographiquement fort (>256 bits)
- [ ] HTTPS obligatoire (TLS 1.3)  
- [ ] Base de données chiffrée au repos
- [ ] Backups chiffrés et testés
- [ ] Rate limiting configuré
- [ ] Monitoring et alertes actifs
- [ ] Scans de vulnérabilité automatisés
- [ ] Rotation des secrets programmée

## 📊 Monitoring & Observabilité

### Métriques applicatives

```python
# Exemple de métriques métier
class CandidatureMetrics:
    candidatures_soumises = Counter('candidatures_soumises_total')
    candidatures_acceptees = Counter('candidatures_acceptees_total') 
    temps_traitement = Histogram('temps_traitement_candidature_seconds')
    notifications_envoyees = Counter('notifications_envoyees_total', ['canal'])
```

### Logs structurés

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "service": "sonamines-candidatures",
  "action": "candidature_soumise",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "offre_id": "660e8400-e29b-41d4-a716-446655440000",
  "duration_ms": 150,
  "metadata": {
    "ip": "192.168.1.100",
    "user_agent": "Mozilla/5.0..."
  }
}
```

### Health Checks

```bash
# Health check complet
curl http://localhost:8000/health

# Réponse JSON détaillée
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "services": {
    "database": "healthy",
    "elasticsearch": "healthy", 
    "minio": "healthy"
  },
  "version": "1.0.0",
  "uptime_seconds": 3600
}
```

## 🤝 Contribution

### Workflow de contribution

1. **🍴 Fork** du repository
2. **🌿 Branche feature** : `git checkout -b feature/ma-fonctionnalite`
3. **💻 Développement** en suivant les standards
4. **🧪 Tests** : coverage > 90%
5. **📝 Documentation** mise à jour
6. **🔍 Pull Request** avec description détaillée

### Standards de code

```bash
# Formatting automatique
black src/ tests/
isort src/ tests/

# Vérification types
mypy src/

# Linting
flake8 src/ tests/

# Tests et couverture
pytest --cov=src --cov-fail-under=90
```

### Template de Pull Request

```markdown
## 📝 Description
Description claire des changements

## 🎯 Type de changement
- [ ] Bug fix
- [ ] Nouvelle fonctionnalité  
- [ ] Breaking change
- [ ] Documentation

## 🧪 Tests
- [ ] Tests unitaires ajoutés/modifiés
- [ ] Tests d'intégration mis à jour
- [ ] Coverage maintenue > 90%

## 📋 Checklist
- [ ] Code formaté (black, isort)
- [ ] Types vérifiés (mypy)
- [ ] Documentation mise à jour
- [ ] Migration DB si nécessaire
- [ ] Changelog mis à jour
```

## 📚 Documentation technique

### 🔗 Liens utiles

- **[FastAPI Documentation](https://fastapi.tiangolo.com)**
- **[SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/)**
- **[Pydantic V2](https://docs.pydantic.dev/2.0/)**
- **[Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)**
- **[Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)**

### 📖 Guides spécialisés

- **[Guide d'architecture hexagonale](docs/hexagonal-architecture.md)**
- **[Patterns et bonnes pratiques](docs/patterns.md)**
- **[Guide de performance](docs/performance.md)**
- **[Troubleshooting](docs/troubleshooting.md)**

## 🏆 Équipe & Crédits

### 👥 Équipe de développement

- **Architecture & Backend** : Équipe IT SONAMINES
- **DevOps & Infrastructure** : Équipe Infrastructure
- **Sécurité** : Équipe Cybersécurité
- **Tests & Qualité** : Équipe QA

### 🙏 Remerciements

Merci aux contributeurs open source des technologies utilisées et à la communauté Python pour les outils exceptionnels.

---

## 📄 Licence

© 2024 SONAMINES. Tous droits réservés.

> **🎯 Mission** : Simplifier et moderniser le processus de recrutement chez SONAMINES avec une technologie de pointe et une expérience utilisateur exceptionnelle.

---

**[⬆ Retour au sommaire](#-table-des-matières)**