"""empty message

Revision ID: 411cc0fc2991
Revises: a9dd28f554d4
Create Date: 2023-03-08 18:03:07.800608

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '411cc0fc2991'
down_revision = 'a9dd28f554d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pokemon',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('poke_name', sa.String(), nullable=False),
    sa.Column('ability', sa.String(), nullable=True),
    sa.Column('sprite_url', sa.String(), nullable=True),
    sa.Column('exp', sa.Integer(), nullable=True),
    sa.Column('attack', sa.Integer(), nullable=True),
    sa.Column('hp', sa.Integer(), nullable=True),
    sa.Column('defense', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('poke_team',
    sa.Column('poke_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['poke_id'], ['pokemon.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('poke_team')
    op.drop_table('pokemon')
    # ### end Alembic commands ###
