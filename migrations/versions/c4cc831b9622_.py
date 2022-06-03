"""empty message

Revision ID: c4cc831b9622
Revises: ab4ffe6bbfe8
Create Date: 2022-06-03 19:29:42.142696

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4cc831b9622'
down_revision = 'ab4ffe6bbfe8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('artists', 'website',
               existing_type=sa.VARCHAR(length=200),
               nullable=False)
    op.alter_column('artists', 'facebook_link',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('artists', 'seeking_venue',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.alter_column('artists', 'seeking_description',
               existing_type=sa.VARCHAR(length=300),
               nullable=False)
    op.alter_column('venues', 'facebook_link',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('venues', 'website',
               existing_type=sa.VARCHAR(length=200),
               nullable=False)
    op.alter_column('venues', 'seeking_talent',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.alter_column('venues', 'seeking_description',
               existing_type=sa.VARCHAR(length=300),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('venues', 'seeking_description',
               existing_type=sa.VARCHAR(length=300),
               nullable=True)
    op.alter_column('venues', 'seeking_talent',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('venues', 'website',
               existing_type=sa.VARCHAR(length=200),
               nullable=True)
    op.alter_column('venues', 'facebook_link',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('artists', 'seeking_description',
               existing_type=sa.VARCHAR(length=300),
               nullable=True)
    op.alter_column('artists', 'seeking_venue',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('artists', 'facebook_link',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('artists', 'website',
               existing_type=sa.VARCHAR(length=200),
               nullable=True)
    # ### end Alembic commands ###
