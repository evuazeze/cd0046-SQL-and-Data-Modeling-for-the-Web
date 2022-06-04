"""empty message

Revision ID: 3b8bf43c5b89
Revises: 146ec07f41e5
Create Date: 2022-06-03 22:53:05.091473

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b8bf43c5b89'
down_revision = '146ec07f41e5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shows', sa.Column('venues_id', sa.Integer(), nullable=True))
    op.alter_column('shows', 'artist_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.create_foreign_key(None, 'shows', 'venues', ['venues_id'], ['id'])
    op.create_foreign_key(None, 'shows', 'artists', ['artist_id'], ['id'])
    op.drop_column('shows', 'venue_id')
    op.drop_column('shows', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shows', sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.add_column('shows', sa.Column('venue_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'shows', type_='foreignkey')
    op.drop_constraint(None, 'shows', type_='foreignkey')
    op.alter_column('shows', 'artist_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_column('shows', 'venues_id')
    # ### end Alembic commands ###
