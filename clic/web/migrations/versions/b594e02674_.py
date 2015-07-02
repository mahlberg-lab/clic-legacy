"""empty message

Revision ID: b594e02674
Revises: f55565299f2
Create Date: 2015-06-08 19:28:08.862049

"""

# revision identifiers, used by Alembic.
revision = 'b594e02674'
down_revision = 'f55565299f2'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('annotations', sa.Column('notes', sa.Text(), nullable=True))
    op.add_column('annotations', sa.Column('proxinfo', sa.String(length=50), nullable=True))
    op.drop_column('annotations', 'note')
    op.drop_column('annotations', 'name')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('annotations', sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('annotations', sa.Column('note', sa.TEXT(), autoincrement=False, nullable=True))
    op.drop_column('annotations', 'proxinfo')
    op.drop_column('annotations', 'notes')
    ### end Alembic commands ###
