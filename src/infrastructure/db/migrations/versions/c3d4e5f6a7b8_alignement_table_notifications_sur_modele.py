"""Alignement table notifications sur le modèle Notification

Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
Create Date: 2026-08-12 10:53:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'c3d4e5f6a7b8'
down_revision: Union[str, None] = 'b2c3d4e5f6a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Aligne notifications sur le modèle Notification (table vide)."""
    # La table notifications est VIDE (0 ligne vérifié) : les colonnes
    # NOT NULL peuvent être ajoutées sans server_default, et la suppression
    # des colonnes obsolètes ne perd aucune donnée.

    # Le type ENUM typeevenement n'existe pas encore en base : on le crée
    # (valeurs issues de TypeEvenement, ordre du domaine).
    op.execute(
        "CREATE TYPE typeevenement AS ENUM ("
        "'COMPTE_CREE', 'COMPTE_VALIDE', 'MOT_DE_PASSE_REINITIALISE', "
        "'CANDIDATURE_RECUE', 'CANDIDATURE_DOSSIER_COMPLET', "
        "'CANDIDATURE_PRESELECTIONNEE', 'CANDIDATURE_CONVOQUEE', "
        "'CANDIDATURE_SELECTIONNEE', 'CANDIDATURE_REJETEE', "
        "'NOUVELLE_OFFRE_PUBLIEE', 'OFFRE_CLOTUREE')"
    )

    # 1. Ajouter les colonnes manquantes
    op.add_column('notifications', sa.Column('type_evenement', postgresql.ENUM(name='typeevenement'), nullable=False))
    op.add_column('notifications', sa.Column('contenu', sa.Text(), nullable=False))
    op.add_column('notifications', sa.Column('statut_lu', sa.Boolean(), nullable=False, server_default=sa.false()))

    # 2. Supprimer l'ancien index sur l'ancienne colonne lue
    op.drop_index('ix_notifications_lue', table_name='notifications')

    # 3. Supprimer les colonnes obsolètes
    op.drop_column('notifications', 'type_notification')
    op.drop_column('notifications', 'titre')
    op.drop_column('notifications', 'message')
    op.drop_column('notifications', 'envoyee')
    op.drop_column('notifications', 'date_envoi')
    op.drop_column('notifications', 'donnees_contexte')
    op.drop_column('notifications', 'lue')

    # 4. Index pertinent pour lister_non_lues_par_utilisateur et
    #    compter_non_lues_par_utilisateur (filtrent par utilisateur_id ET
    #    statut_lu=False) : un index composite sur (utilisateur_id, statut_lu)
    #    sert directement ces requêtes du port.
    op.create_index(
        'ix_notifications_utilisateur_statut_lu',
        'notifications',
        ['utilisateur_id', 'statut_lu'],
    )


def downgrade() -> None:
    """Inverse : recrée l'ancien schéma notifications."""
    # LIMITES : si la table contenait des lignes au moment du downgrade,
    # les colonnes NOT NULL recréées (titre, message, lue, envoyee)
    # seraient remplies sans valeur (perte de données) et la conversion
    # typeevenement -> typenotification n'est pas gérée ici. La table est
    # actuellement vide, ce downgrade est donc sans perte à ce stade.
    # Le type ENUM typeevenement est recréé volontairement.

    # 1. Supprimer l'index composite
    op.drop_index('ix_notifications_utilisateur_statut_lu', table_name='notifications')

    # 2. Recréer l'index sur l'ancienne colonne lue (après sa recréation)
    # 3. Supprimer les colonnes du nouveau modèle
    op.drop_column('notifications', 'statut_lu')
    op.drop_column('notifications', 'contenu')
    op.drop_column('notifications', 'type_evenement')

    # 4. Recréer les colonnes obsolètes avec leurs caractéristiques d'origine
    op.add_column('notifications', sa.Column('lue', sa.Boolean(), nullable=False))
    op.add_column('notifications', sa.Column('donnees_contexte', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.add_column('notifications', sa.Column('date_envoi', postgresql.TIMESTAMP(), nullable=True))
    op.add_column('notifications', sa.Column('envoyee', sa.Boolean(), nullable=False))
    op.add_column('notifications', sa.Column('message', sa.Text(), nullable=False))
    op.add_column('notifications', sa.Column('titre', sa.VARCHAR(), nullable=False))
    op.add_column('notifications', sa.Column('type_notification', postgresql.ENUM('CONFIRMATION_INSCRIPTION', 'CANDIDATURE_RECUE', 'STATUT_CANDIDATURE', 'NOUVEAU_MESSAGE', 'RAPPEL', name='typenotification'), nullable=False))

    # 5. Recréer l'index sur l'ancienne colonne lue
    op.create_index('ix_notifications_lue', 'notifications', ['lue'])

    # Le type ENUM typeevenement est laissé en place (sa suppression est
    # facultative ; on évite un DROP TYPE potentiellement risqué si une
    # autre utilisation existait).
