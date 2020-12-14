"""QuestionType table

Revision ID: fab500308f2c
Revises: 
Create Date: 2020-12-14 11:28:59.563469

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fab500308f2c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('QuestionType',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('function', sa.String(length=128), nullable=True),
    sa.Column('form', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('QuestionType')
    # ### end Alembic commands ###
