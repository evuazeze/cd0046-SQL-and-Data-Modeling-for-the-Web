"""empty message

Revision ID: 9cf89a467d18
Revises: ad5a6639f5c3
Create Date: 2022-06-06 19:48:29.100908

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9cf89a467d18'
down_revision = 'ad5a6639f5c3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('artist_shows')
    op.drop_table('shows')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shows',
    sa.Column('start_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('venue_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['venue_id'], ['venues.id'], name='shows_venue_id_fkey')
    )
    op.create_table('artist_shows',
    sa.Column('artist_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['artists.id'], name='artist_shows_artist_id_fkey'),
    sa.PrimaryKeyConstraint('artist_id', name='artist_shows_pkey')
    )
    # ### end Alembic commands ###