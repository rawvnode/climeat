"""create cities, city_responses tables

Revision ID: 55196e022f65
Revises: 
Create Date: 2021-10-21 12:05:03.798461

"""
from enum import auto
from re import T
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55196e022f65'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('cities'
        , sa.Column('id', sa.Integer(), autoincrement=True, nullable=False)
        , sa.Column('account_number', sa.Integer(), nullable=False)
        , sa.Column('year_reported', sa.Integer(), nullable=False)
        , sa.Column('organization', sa.String(length=256), nullable=False)
        , sa.Column('city', sa.String(length=512), nullable=False)
        , sa.Column('country', sa.String(length=512), nullable=False)
        , sa.Column('cdp_region', sa.String(length=512), nullable=False)
        , sa.Column('reporting_authority', sa.String(length=512), nullable=False)
        , sa.Column('access', sa.String(length=256), nullable=False)
        , sa.Column('first_time_discloser', sa.String(length=256), nullable=False)
        , sa.Column('population_year', sa.Integer(), nullable=False)
        , sa.Column('population', sa.Integer(), nullable=False)
        , sa.Column('created_at'
                , sa.DateTime()
                , nullable=False
                , server_default=sa.sql.func.now())
        , sa.PrimaryKeyConstraint('id')
    )

    op.create_table('city_responses'
        , sa.Column('id', sa.Integer(), autoincrement=True, nullable=False)
        , sa.Column('account_number', sa.Integer(), nullable=False)
        , sa.Column('year_reported', sa.Integer(), nullable=False)
        , sa.Column('organization', sa.String(length=256), nullable=False)
        , sa.Column('country', sa.String(length=512), nullable=False)
        , sa.Column('cdp_region', sa.String(length=512), nullable=False)
        , sa.Column('parent_section', sa.String(length=512), nullable=False)
        , sa.Column('section', sa.String(length=512), nullable=False)
        , sa.Column('question_number', sa.String(length=512), nullable=False)
        , sa.Column('question_name', sa.Text, nullable=False)
        , sa.Column('column_number', sa.Integer, nullable=False)
        , sa.Column('column_name', sa.String(length=512), nullable=False)
        , sa.Column('row_number', sa.Integer, nullable=False)
        , sa.Column('row_name', sa.String(length=512), nullable=False)
        , sa.Column('response_answer', sa.Text, nullable=False)
        , sa.Column('created_at'
                , sa.DateTime()
                , nullable=False
                , server_default=sa.sql.func.now())
        , sa.PrimaryKeyConstraint('id')                
    )

def downgrade():
    pass
