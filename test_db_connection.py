#!/usr/bin/env python3
"""Script de test de connexion à la base de données."""

import asyncio
import sys
from pathlib import Path

# Ajouter le répertoire racine au PYTHONPATH
sys.path.append(str(Path(__file__).parent))

from src.infrastructure.config import settings


async def test_db_connection():
    """Test de connexion à la base de données PostgreSQL."""
    try:
        import asyncpg
        print(f"🔗 Tentative de connexion à : {settings.database_url}")
        
        # Extraire les paramètres de connexion depuis l'URL
        # Format: postgresql+asyncpg://user:password@host:port/database
        url_parts = settings.database_url.replace("postgresql+asyncpg://", "").split("@")
        user_pass = url_parts[0].split(":")
        host_port_db = url_parts[1].split("/")
        host_port = host_port_db[0].split(":")
        
        user = user_pass[0]
        password = user_pass[1]
        host = host_port[0]
        port = int(host_port[1])
        database = host_port_db[1]
        
        print(f"📊 Paramètres de connexion:")
        print(f"   Host: {host}")
        print(f"   Port: {port}")
        print(f"   Database: {database}")
        print(f"   User: {user}")
        
        # Test de connexion
        conn = await asyncpg.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
        )
        
        # Test de requête simple
        version = await conn.fetchval('SELECT version()')
        print(f"✅ Connexion réussie !")
        print(f"📋 Version PostgreSQL: {version}")
        
        # Test de création d'une table temporaire
        await conn.execute('''
            CREATE TEMPORARY TABLE test_table (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        await conn.execute('''
            INSERT INTO test_table (name) VALUES ($1)
        ''', 'Test de connexion SONAMINES')
        
        result = await conn.fetchrow('SELECT * FROM test_table WHERE name = $1', 'Test de connexion SONAMINES')
        print(f"🧪 Test d'écriture/lecture: {result}")
        
        await conn.close()
        print("✅ Test de connexion terminé avec succès !")
        
        return True
        
    except ImportError:
        print("❌ Erreur: asyncpg n'est pas installé")
        print("   Pour installer: pip install asyncpg")
        return False
        
    except Exception as e:
        print(f"❌ Erreur de connexion: {type(e).__name__}: {e}")
        print("\n🔧 Solutions possibles:")
        print("   1. Vérifier que PostgreSQL est démarré")
        print("   2. Vérifier les paramètres de connexion dans .env")
        print("   3. Démarrer PostgreSQL avec Docker:")
        print("      docker run -d --name postgres-test \\")
        print("        -e POSTGRES_USER=postgres \\")
        print("        -e POSTGRES_PASSWORD=postgres \\")
        print("        -e POSTGRES_DB=sonamines_candidatures_test \\")
        print("        -p 5432:5432 postgres:15")
        return False


async def test_config_loading():
    """Test de chargement de la configuration."""
    try:
        print("🔧 Test de chargement de la configuration:")
        print(f"   Database URL: {settings.database_url}")
        print(f"   Elasticsearch URL: {settings.elasticsearch_url}")
        print(f"   MinIO Endpoint: {settings.minio_endpoint}")
        print(f"   JWT Secret (preview): {settings.jwt_secret_key[:10]}...")
        print(f"   Max taille document: {settings.max_taille_document_mo} Mo")
        print(f"   Max taille photo: {settings.max_taille_photo_mo} Mo")
        print(f"   Formats documents: {settings.formats_documents_autorises_list}")
        print(f"   Formats photos: {settings.formats_photo_autorises_list}")
        print("✅ Configuration chargée avec succès !")
        return True
    except Exception as e:
        print(f"❌ Erreur de configuration: {e}")
        return False


async def main():
    """Fonction principale du test."""
    print("🚀 Test de l'infrastructure SONAMINES")
    print("=" * 50)
    
    # Test 1: Configuration
    print("\n1️⃣ Test de configuration:")
    config_ok = await test_config_loading()
    
    # Test 2: Base de données
    print("\n2️⃣ Test de connexion base de données:")
    if config_ok:
        db_ok = await test_db_connection()
    else:
        print("❌ Test de base ignoré (configuration invalide)")
        db_ok = False
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 Résumé des tests:")
    print(f"   Configuration: {'✅ OK' if config_ok else '❌ ERREUR'}")
    print(f"   Base de données: {'✅ OK' if db_ok else '❌ ERREUR'}")
    
    if config_ok and db_ok:
        print("\n🎉 Tous les tests passent ! Infrastructure prête.")
        return 0
    else:
        print("\n⚠️  Certains tests ont échoué. Vérifiez la configuration.")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))