"""Added company and email to case model

Revision ID: 49301064e852
Revises: 0dafc6d9292d
Create Date: 2021-03-24 10:56:12.897915

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49301064e852'
down_revision = '0dafc6d9292d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Case', sa.Column('company', sa.String(), nullable=True))
    op.add_column('Case', sa.Column('email', sa.String(), nullable=True))
    op.create_index(op.f('ix_Case_company'), 'Case', ['company'], unique=False)
    op.create_index(op.f('ix_Case_start'), 'Case', ['start'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_Case_start'), table_name='Case')
    op.drop_index(op.f('ix_Case_company'), table_name='Case')
    op.drop_column('Case', 'email')
    op.drop_column('Case', 'company')
    # ### end Alembic commands ###