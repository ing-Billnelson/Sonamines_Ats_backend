"""Création initiale des tables

Revision ID: 1fbd1d88b789
Revises: 
Create Date: 2026-08-07 07:07:42.106775

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '1fbd1d88b789'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Création de l'extension UUID si elle n'existe pas
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    
    # Table utilisateurs
    op.create_table('utilisateurs',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('telephone', sa.String(), nullable=True),
        sa.Column('mot_de_passe_hash', sa.String(), nullable=False),
        sa.Column('nom', sa.String(), nullable=False),
        sa.Column('prenom', sa.String(), nullable=False),
        sa.Column('statut', sa.Enum('EN_ATTENTE_VALIDATION', 'ACTIF', 'SUSPENDU', name='statutcompte'), nullable=False),
        sa.Column('canal_validation', sa.Enum('EMAIL', 'SMS', name='canalnotification'), nullable=False),
        sa.Column('email_verifie', sa.Boolean(), nullable=False, default=False),
        sa.Column('telephone_verifie', sa.Boolean(), nullable=False, default=False),
        sa.Column('date_creation', sa.DateTime(), nullable=False),
        sa.Column('date_derniere_connexion', sa.DateTime(), nullable=True),
        sa.Column('date_modification', sa.DateTime(), nullable=True),
        sa.Column('type_utilisateur', sa.String(50), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_utilisateurs_email'), 'utilisateurs', ['email'], unique=True)

    # Table offres
    op.create_table('offres',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('titre', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('departement', sa.String(), nullable=False),
        sa.Column('lieu', sa.String(), nullable=False),
        sa.Column('salaire_min', sa.Integer(), nullable=True),
        sa.Column('salaire_max', sa.Integer(), nullable=True),
        sa.Column('type_contrat', sa.Enum('CDI', 'CDD', 'STAGE', 'FREELANCE', name='typecontrat'), nullable=False),
        sa.Column('niveau_experience', sa.Enum('JUNIOR', 'CONFIRME', 'SENIOR', 'EXPERT', name='niveauexperience'), nullable=False),
        sa.Column('statut', sa.Enum('BROUILLON', 'PUBLIE', 'FERME', 'ARCHIVE', name='statutoffre'), nullable=False),
        sa.Column('date_publication', sa.DateTime(), nullable=True),
        sa.Column('date_cloture', sa.DateTime(), nullable=True),
        sa.Column('competences_requises', sa.JSON(), nullable=True),
        sa.Column('date_creation', sa.DateTime(), nullable=False),
        sa.Column('date_modification', sa.DateTime(), nullable=True),
        sa.Column('creee_par_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(['creee_par_id'], ['utilisateurs.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Table candidatures
    op.create_table('candidatures',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('candidat_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('offre_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('statut', sa.Enum('SOUMISE', 'EN_COURS', 'ACCEPTEE', 'REFUSEE', 'RETIREE', name='statutcandidature'), nullable=False),
        sa.Column('lettre_motivation', sa.Text(), nullable=True),
        sa.Column('date_candidature', sa.DateTime(), nullable=False),
        sa.Column('date_modification', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['candidat_id'], ['utilisateurs.id'], ),
        sa.ForeignKeyConstraint(['offre_id'], ['offres.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_candidatures_candidat_id'), 'candidatures', ['candidat_id'])
    op.create_index(op.f('ix_candidatures_offre_id'), 'candidatures', ['offre_id'])
    # Index unique pour éviter les doublons candidat-offre
    op.create_index('ix_candidatures_candidat_offre_unique', 'candidatures', ['candidat_id', 'offre_id'], unique=True)

    # Table documents
    op.create_table('documents',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('nom_fichier', sa.String(), nullable=False),
        sa.Column('nom_original', sa.String(), nullable=False),
        sa.Column('type_document', sa.Enum('CV', 'LETTRE_MOTIVATION', 'DIPLOME', 'CERTIFICAT', 'AUTRE', name='typedocument'), nullable=False),
        sa.Column('type_fichier', sa.Enum('DOCUMENT', 'PHOTO', name='typefichier'), nullable=False),
        sa.Column('taille', sa.Integer(), nullable=False),
        sa.Column('format_fichier', sa.String(), nullable=False),
        sa.Column('chemin_stockage', sa.String(), nullable=False),
        sa.Column('utilisateur_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('candidature_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('date_upload', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['candidature_id'], ['candidatures.id'], ),
        sa.ForeignKeyConstraint(['utilisateur_id'], ['utilisateurs.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_documents_utilisateur_id'), 'documents', ['utilisateur_id'])
    op.create_index(op.f('ix_documents_candidature_id'), 'documents', ['candidature_id'])

    # Table historique_statuts
    op.create_table('historique_statuts',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('candidature_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('ancien_statut', sa.Enum('SOUMISE', 'EN_COURS', 'ACCEPTEE', 'REFUSEE', 'RETIREE', name='statutcandidature'), nullable=True),
        sa.Column('nouveau_statut', sa.Enum('SOUMISE', 'EN_COURS', 'ACCEPTEE', 'REFUSEE', 'RETIREE', name='statutcandidature'), nullable=False),
        sa.Column('commentaire', sa.Text(), nullable=True),
        sa.Column('modifie_par_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('date_changement', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['candidature_id'], ['candidatures.id'], ),
        sa.ForeignKeyConstraint(['modifie_par_id'], ['utilisateurs.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_historique_statuts_candidature_id'), 'historique_statuts', ['candidature_id'])

    # Table notifications
    op.create_table('notifications',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('utilisateur_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('type_notification', sa.Enum('CONFIRMATION_INSCRIPTION', 'CANDIDATURE_RECUE', 'STATUT_CANDIDATURE', 'NOUVEAU_MESSAGE', 'RAPPEL', name='typenotification'), nullable=False),
        sa.Column('canal', sa.Enum('EMAIL', 'SMS', name='canalnotification'), nullable=False),
        sa.Column('titre', sa.String(), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('lue', sa.Boolean(), nullable=False, default=False),
        sa.Column('envoyee', sa.Boolean(), nullable=False, default=False),
        sa.Column('date_creation', sa.DateTime(), nullable=False),
        sa.Column('date_lecture', sa.DateTime(), nullable=True),
        sa.Column('date_envoi', sa.DateTime(), nullable=True),
        sa.Column('donnees_contexte', sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['utilisateur_id'], ['utilisateurs.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notifications_utilisateur_id'), 'notifications', ['utilisateur_id'])
    op.create_index(op.f('ix_notifications_lue'), 'notifications', ['lue'])


def downgrade() -> None:
    # Suppression des tables dans l'ordre inverse (contraintes FK)
    op.drop_table('notifications')
    op.drop_table('historique_statuts')
    op.drop_table('documents')
    op.drop_table('candidatures')
    op.drop_table('offres')
    op.drop_table('utilisateurs')
    
    # Suppression des enums
    op.execute('DROP TYPE IF EXISTS typenotification')
    op.execute('DROP TYPE IF EXISTS canalnotification')
    op.execute('DROP TYPE IF EXISTS typefichier')
    op.execute('DROP TYPE IF EXISTS typedocument')
    op.execute('DROP TYPE IF EXISTS statutcandidature')
    op.execute('DROP TYPE IF EXISTS statutoffre')
    op.execute('DROP TYPE IF EXISTS niveauexperience')
    op.execute('DROP TYPE IF EXISTS typecontrat')
    op.execute('DROP TYPE IF EXISTS statutcompte')
