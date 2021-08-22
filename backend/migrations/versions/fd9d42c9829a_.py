"""empty message

Revision ID: fd9d42c9829a
Revises: 9559b70a8c87
Create Date: 2021-05-26 14:12:10.594429

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd9d42c9829a'
down_revision = '9559b70a8c87'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('services',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('service_name', sa.String(length=50), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('service_name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('services')
    # ### end Alembic commands ###