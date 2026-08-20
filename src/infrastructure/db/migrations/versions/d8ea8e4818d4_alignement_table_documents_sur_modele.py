"""Alignement table documents sur le modele

Revision ID: d8ea8e4818d4
Revises: 02052f8cc6e9
Create Date: 2026-08-19 21:49:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd8ea8e4818d4'
down_revision: Union[str, None] = '02052f8cc6e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Aligne la table documents sur le modèle DocumentModel.

    Renomme les colonnes obsolètes, ajoute type_mime, rend candidature_id
    obligatoire et supprime les colonnes mortes type_fichier / format_fichier.

    Préconditions vérifiées avant rédaction (base sonamines_candidatures) :
      - la table documents est vide (0 ligne) -> type_mime peut être
        nullable=False directement ;
      - aucune ligne avec candidature_id NULL -> candidature_id peut être
        rendu nullable=False sans risque.
    Si ces préconditions ne sont pas vérifiées dans un autre environnement,
    adapter la nullabilité de type_mime et de candidature_id.
    """
    # 1. Renommer nom_fichier en nom_fichier_stockage
    op.alter_column('documents', 'nom_fichier', new_column_name='nom_fichier_stockage')

    # 2. Renommer chemin_stockage en url_stockage
    op.alter_column('documents', 'chemin_stockage', new_column_name='url_stockage')

    # 3. Renommer taille en taille_octets
    op.alter_column('documents', 'taille', new_column_name='taille_octets')

    # 4. Renommer utilisateur_id en telechargeur_id
    #    (supprime la FK existante, renomme la colonne, recrée la FK)
    op.drop_constraint(
        'documents_utilisateur_id_fkey',
        'documents',
        type_='foreignkey',
    )
    op.alter_column('documents', 'utilisateur_id', new_column_name='telechargeur_id')
    op.create_foreign_key(
        'documents_telechargeur_id_fkey',
        'documents',
        'utilisateurs',
        ['telechargeur_id'],
        ['id'],
    )

    # 5. Renommer date_upload en date_telechargement
    op.alter_column('documents', 'date_upload', new_column_name='date_telechargement')

    # 6. Ajouter type_mime (nullable=False, table vide)
    op.add_column(
        'documents',
        sa.Column('type_mime', sa.String(100), nullable=False),
    )

    # 7. Rendre candidature_id obligatoire (aucune valeur NULL en base)
    op.alter_column(
        'documents',
        'candidature_id',
        existing_type=postgresql.UUID(as_uuid=True),
        nullable=False,
    )

    # 8. Supprimer les colonnes mortes type_fichier et format_fichier
    #    (confirmées inutilisées dans tout le code applicatif)
    op.drop_column('documents', 'format_fichier')
    op.drop_column('documents', 'type_fichier')


def downgrade() -> None:
    """Inverse l'alignement.

    ATTENTION : limites documentées (équivalentes aux migrations précédentes) :
      - type_mime est supprimé : les valeurs éventuellement stockées y sont
        perdues (données non triviales) ;
      - la colonne type_fichier fait référence à l'enum 'typefichier'
        (DOCUMENT/PHOTO) toujours présent en base après l'upgrade ;
      - les autres colonnes sont restaurées à leurs caractéristiques
        d'origine (candidature_id repasse nullable=True).
    """
    # 8 (inverse). Ré-ajouter type_fichier et format_fichier
    op.add_column(
        'documents',
        sa.Column(
            'format_fichier',
            sa.String(),
            nullable=False,
            server_default='',
        ),
    )
    op.add_column(
        'documents',
        sa.Column(
            'type_fichier',
            postgresql.ENUM('DOCUMENT', 'PHOTO', name='typefichier', create_type=False),
            nullable=False,
            server_default='DOCUMENT',
        ),
    )

    # 7 (inverse). Rendre candidature_id de nouveau nullable
    op.alter_column(
        'documents',
        'candidature_id',
        existing_type=postgresql.UUID(as_uuid=True),
        nullable=True,
    )

    # 6 (inverse). Supprimer type_mime
    op.drop_column('documents', 'type_mime')

    # 5 (inverse). Renommer date_telechargement en date_upload
    op.alter_column('documents', 'date_telechargement', new_column_name='date_upload')

    # 4 (inverse). Renommer telechargeur_id en utilisateur_id (avec FK recréée)
    op.drop_constraint(
        'documents_telechargeur_id_fkey',
        'documents',
        type_='foreignkey',
    )
    op.alter_column('documents', 'telechargeur_id', new_column_name='utilisateur_id')
    op.create_foreign_key(
        'documents_utilisateur_id_fkey',
        'documents',
        'utilisateurs',
        ['utilisateur_id'],
        ['id'],
    )

    # 3 (inverse). Renommer taille_octets en taille
    op.alter_column('documents', 'taille_octets', new_column_name='taille')

    # 2 (inverse). Renommer url_stockage en chemin_stockage
    op.alter_column('documents', 'url_stockage', new_column_name='chemin_stockage')

    # 1 (inverse). Renommer nom_fichier_stockage en nom_fichier
    op.alter_column('documents', 'nom_fichier_stockage', new_column_name='nom_fichier')
