"""empty message

Revision ID: b6cd8be0522
Revises: 1b3d6e1706f
Create Date: 2015-06-08 15:15:11.256592

"""

# revision identifiers, used by Alembic.
revision = 'b6cd8be0522'
down_revision = '1b3d6e1706f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('annotations', sa.Column('category_id', sa.Integer(), nullable=True))
    op.add_column('annotations', sa.Column('note', sa.Text(), nullable=True))
    op.create_foreign_key(None, 'annotations', 'annotation_categories', ['category_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'annotations', type_='foreignkey')
    op.drop_column('annotations', 'note')
    op.drop_column('annotations', 'category_id')
    ### end Alembic commands ###
