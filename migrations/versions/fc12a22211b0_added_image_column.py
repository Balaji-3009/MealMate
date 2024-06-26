"""added image column

Revision ID: fc12a22211b0
Revises: 5e078c0b50c6
Create Date: 2024-02-24 19:30:54.034562

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc12a22211b0'
down_revision = '5e078c0b50c6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('menu', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('menu', schema=None) as batch_op:
        batch_op.drop_column('image')

    # ### end Alembic commands ###
