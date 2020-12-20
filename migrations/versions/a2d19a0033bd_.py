"""empty message

Revision ID: a2d19a0033bd
Revises: 2505184abaec
Create Date: 2020-12-07 00:15:35.314992

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a2d19a0033bd'
down_revision = '2505184abaec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('venues', 'image_link',
               existing_type=sa.VARCHAR(length=500),
               nullable=True)
    op.alter_column('venues', 'seeking_description',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('venues', 'seeking_talent',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('venues', 'website',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_column('venues', 'genres')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venues', sa.Column('genres', postgresql.BYTEA(), autoincrement=False, nullable=False))
    op.alter_column('venues', 'website',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('venues', 'seeking_talent',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.alter_column('venues', 'seeking_description',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('venues', 'image_link',
               existing_type=sa.VARCHAR(length=500),
               nullable=False)
    # ### end Alembic commands ###