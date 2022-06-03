"""empty message

Revision ID: 146ec07f41e5
Revises: 4b554b085850
Create Date: 2022-06-03 22:12:41.365307

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '146ec07f41e5'
down_revision = '4b554b085850'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shows',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('shows')
    # ### end Alembic commands ###
