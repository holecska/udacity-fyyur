"""empty message

Revision ID: 7b188b61b6f0
Revises: 60fc440a097d
Create Date: 2020-12-08 22:54:52.462556

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b188b61b6f0'
down_revision = '60fc440a097d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shows', sa.Column('artist_id', sa.Integer(), nullable=False))
    op.add_column('shows', sa.Column('venue_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'shows', 'artists', ['artist_id'], ['id'])
    op.create_foreign_key(None, 'shows', 'venues', ['venue_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'shows', type_='foreignkey')
    op.drop_constraint(None, 'shows', type_='foreignkey')
    op.drop_column('shows', 'venue_id')
    op.drop_column('shows', 'artist_id')
    # ### end Alembic commands ###
