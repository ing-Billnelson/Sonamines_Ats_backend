"""Alignement table offres sur le modèle domaine

Revision ID: a1b2c3d4e5f6
Revises: f7ca4d6b3e09
Create Date: 2026-08-11 12:50:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = 'f7ca4d6b3e09'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Aligne la table offres sur le modèle Offre."""
    # La table offres est VIDE (0 ligne vérifié avant rédaction) : les
    # colonnes NOT NULL peuvent être ajoutées sans server_default, et la
    # conversion competences_requises est simple (aucune donnée à migrer).

    # Les types ENUM typeoffre/typestage n'existent pas encore en base.
    op.execute("CREATE TYPE typeoffre AS ENUM ('EMPLOI', 'STAGE')")
    op.execute("CREATE TYPE typestage AS ENUM ('ACADEMIQUE', 'PROFESSIONNEL')")

    # 1. Ajouter les colonnes manquantes
    op.add_column('offres', sa.Column('numero_reference', sa.String(length=50), nullable=False))
    op.add_column('offres', sa.Column('type_offre', postgresql.ENUM(name='typeoffre'), nullable=False))
    op.add_column('offres', sa.Column('type_stage', postgresql.ENUM(name='typestage'), nullable=True))
    op.add_column('offres', sa.Column('experience_requise', sa.Text(), nullable=True))
    op.add_column('offres', sa.Column('date_limite_candidature', sa.DateTime(), nullable=True))

    # 2. Renommer creee_par_id -> createur_id (FK vers utilisateurs.id)
    op.drop_constraint('offres_creee_par_id_fkey', 'offres', type_='foreignkey')
    op.alter_column('offres', 'creee_par_id', new_column_name='createur_id')
    op.create_foreign_key(
        'offres_createur_id_fkey', 'offres', 'utilisateurs',
        ['createur_id'], ['id'],
    )

    # 3. type_contrat devient nullable (seulement pour les emplois)
    op.alter_column(
        'offres', 'type_contrat',
        existing_type=postgresql.ENUM('CDI', 'CDD', 'STAGE', 'FREELANCE', name='typecontrat'),
        nullable=True,
    )

    # 4. salaire_min / salaire_max : Integer -> Float
    op.alter_column('offres', 'salaire_min',
                    existing_type=sa.Integer(), type_=sa.Float(), existing_nullable=True)
    op.alter_column('offres', 'salaire_max',
                    existing_type=sa.Integer(), type_=sa.Float(), existing_nullable=True)

    # 5. competences_requises : JSON -> ARRAY(String).
    #    Table vide => conversion simple vers un tableau vide, aucune
    #    extraction JSON à faire.
    op.execute(
        "ALTER TABLE offres ALTER COLUMN competences_requises "
        "TYPE VARCHAR[] USING ARRAY[]::VARCHAR[]"
    )

    # 6. Supprimer les colonnes mortes (inutilisées dans le code)
    op.drop_column('offres', 'departement')
    op.drop_column('offres', 'niveau_experience')

    # 7. Index unique sur numero_reference
    op.create_index(op.f('ix_offres_numero_reference'), 'offres', ['numero_reference'], unique=True)


def downgrade() -> None:
    """Retour le plus fidèle possible vers l'ancien schéma."""
    # LIMITES du downgrade :
    # - competences_requises : conversion ARRAY -> JSON via to_json() : la
    #   structure JSON d'origine n'est pas restaurée (perte sémantique).
    # - salaire_min/max : Float -> Integer peut tronquer des valeurs non
    #   entières.
    # - departement / niveau_experience n'existent plus dans le code ; on
    #   les recrée NOT NULL avec un server_default de repli.
    # - type_contrat repasse en NOT NULL : peut échouer si des lignes ont
    #   type_contrat NULL au moment du downgrade.

    # 1. Index unique
    op.drop_index(op.f('ix_offres_numero_reference'), table_name='offres')

    # 2. Recréer les colonnes mortes (NOT NULL => server_default de repli)
    op.add_column('offres', sa.Column('departement', sa.VARCHAR(), nullable=False, server_default=''))
    op.add_column(
        'offres', sa.Column(
            'niveau_experience',
            postgresql.ENUM('JUNIOR', 'CONFIRME', 'SENIOR', 'EXPERT', name='niveauexperience'),
            nullable=False, server_default='JUNIOR',
        ),
    )

    # 3. competences_requises : ARRAY -> JSON (conversion simple ; perte de la structure)
    op.execute(
        "ALTER TABLE offres ALTER COLUMN competences_requises "
        "TYPE JSON USING to_json(competences_requises)"
    )

    # 4. salaire Float -> Integer (troncature possible)
    op.alter_column('offres', 'salaire_min', existing_type=sa.Float(), type_=sa.Integer(), existing_nullable=True)
    op.alter_column('offres', 'salaire_max', existing_type=sa.Float(), type_=sa.Integer(), existing_nullable=True)

    # 5. type_contrat repasse en NOT NULL (peut échouer si des NULL existent)
    op.alter_column(
        'offres', 'type_contrat',
        existing_type=postgresql.ENUM('CDI', 'CDD', 'STAGE', 'FREELANCE', name='typecontrat'),
        nullable=False,
    )

    # 6. Renommer createur_id -> creee_par_id
    op.drop_constraint('offres_createur_id_fkey', 'offres', type_='foreignkey')
    op.alter_column('offres', 'createur_id', new_column_name='creee_par_id')
    op.create_foreign_key(
        'offres_creee_par_id_fkey', 'offres', 'utilisateurs',
        ['creee_par_id'], ['id'],
    )

    # 7. Supprimer les colonnes ajoutées à l'upgrade
    op.drop_column('offres', 'date_limite_candidature')
    op.drop_column('offres', 'experience_requise')
    op.drop_column('offres', 'type_stage')
    op.drop_column('offres', 'type_offre')
    op.drop_column('offres', 'numero_reference')

    # Les types ENUM typeoffre/typestage sont laissés en place (leur
    # suppression est facultative et sans effet puisque les colonnes sont
    # retirées ; on évite un DROP TYPE potentiellement risqué).
