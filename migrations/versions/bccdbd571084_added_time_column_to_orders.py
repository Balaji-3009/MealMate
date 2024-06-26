"""added time column to orders

Revision ID: bccdbd571084
Revises: d9b1bffcdcc9
Create Date: 2024-03-10 17:00:35.106332

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bccdbd571084'
down_revision = 'd9b1bffcdcc9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('time', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.drop_column('time')

    # ### end Alembic commands ###
