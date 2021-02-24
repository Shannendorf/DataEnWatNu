"""Added code model

Revision ID: 4575217141c4
Revises: b6dc8d9ae1da
Create Date: 2021-02-24 11:09:35.799331

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4575217141c4'
down_revision = 'b6dc8d9ae1da'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Code',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(), nullable=True),
    sa.Column('create_on', sa.DateTime(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Code_code'), 'Code', ['code'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_Code_code'), table_name='Code')
    op.drop_table('Code')
    # ### end Alembic commands ###