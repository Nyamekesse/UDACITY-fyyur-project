"""empty message

Revision ID: 47accd99acc2
Revises: aa1245061650
Create Date: 2022-06-01 20:51:25.144350

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47accd99acc2'
down_revision = 'aa1245061650'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('artist', 'seeking_description')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column('seeking_description', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
