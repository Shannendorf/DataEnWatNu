"""Added questionlist model

Revision ID: 92d3b23fc253
Revises: 4575217141c4
Create Date: 2021-03-01 10:27:28.231830

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92d3b23fc253'
down_revision = '4575217141c4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('QuestionList',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_QuestionList_name'), 'QuestionList', ['name'], unique=True)
    op.create_table('QuestionListQuestionGroup',
    sa.Column('question_list_id', sa.Integer(), nullable=True),
    sa.Column('question_group_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['question_group_id'], ['QuestionGroup.id'], ),
    sa.ForeignKeyConstraint(['question_list_id'], ['QuestionList.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('QuestionListQuestionGroup')
    op.drop_index(op.f('ix_QuestionList_name'), table_name='QuestionList')
    op.drop_table('QuestionList')
    # ### end Alembic commands ###
