# Dockerfile pour l'application SONAMINES Candidatures
# Architecture hexagonale avec FastAPI + PostgreSQL + Elasticsearch + MinIO

# =================================================================
# Stage 1: Builder - Installation des dépendances et build
# =================================================================
FROM python:3.11-slim as builder

LABEL maintainer="SONAMINES IT Team"
LABEL description="Plateforme de candidatures SONAMINES - Architecture hexagonale"

# Variables d'environnement pour le build
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Installation des outils système nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Création du répertoire de travail
WORKDIR /app

# Copie des fichiers de dépendances
COPY requirements.txt requirements-dev.txt ./

# Installation des dépendances Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# =================================================================
# Stage 2: Runtime - Image finale optimisée
# =================================================================
FROM python:3.11-slim as runtime

# Variables d'environnement pour l'exécution
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    PORT=8000

# Installation des dépendances système runtime uniquement
RUN apt-get update && apt-get install -y \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd -r appuser \
    && useradd -r -g appuser -d /app -s /bin/bash appuser

# Copie des dépendances depuis le builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Création de la structure de répertoires
WORKDIR /app
RUN mkdir -p /app/logs /app/uploads /app/tmp \
    && chown -R appuser:appuser /app

# Copie du code source
COPY --chown=appuser:appuser . /app/

# Switch vers l'utilisateur non-root
USER appuser

# Health check pour vérifier que l'application est prête
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$PORT/health || exit 1

# Exposition du port
EXPOSE $PORT

# Script de démarrage
COPY --chown=appuser:appuser docker-entrypoint.sh /app/
RUN chmod +x /app/docker-entrypoint.sh

# Point d'entrée par défaut
ENTRYPOINT ["/app/docker-entrypoint.sh"]

# Commande par défaut : démarrer le serveur FastAPI
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]