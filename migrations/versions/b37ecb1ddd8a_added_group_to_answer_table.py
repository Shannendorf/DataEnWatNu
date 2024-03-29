"""Added group to answer table

Revision ID: b37ecb1ddd8a
Revises: f2c49fd52f8c
Create Date: 2021-03-08 15:04:57.216885

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b37ecb1ddd8a'
down_revision = 'f2c49fd52f8c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Answer', sa.Column('group', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'Answer', 'QuestionGroup', ['group'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Answer', type_='foreignkey')
    op.drop_column('Answer', 'group')
    # ### end Alembic commands ###
