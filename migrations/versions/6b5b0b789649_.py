"""empty message

Revision ID: 6b5b0b789649
Revises: af383e8676ba
Create Date: 2022-06-03 13:26:43.715907

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b5b0b789649'
down_revision = 'af383e8676ba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('artists', 'website',
               existing_type=sa.VARCHAR(length=200),
               nullable=True)
    op.alter_column('artists', 'facebook_link',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('venues', 'facebook_link',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('venues', 'website',
               existing_type=sa.VARCHAR(length=200),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('venues', 'website',
               existing_type=sa.VARCHAR(length=200),
               nullable=False)
    op.alter_column('venues', 'facebook_link',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('artists', 'facebook_link',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('artists', 'website',
               existing_type=sa.VARCHAR(length=200),
               nullable=False)
    # ### end Alembic commands ###
