"""modified time column

Revision ID: 0f8957b92b55
Revises: 1a910e372200
Create Date: 2024-02-25 11:26:52.150597

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f8957b92b55'
down_revision = '1a910e372200'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('menu', schema=None) as batch_op:
        batch_op.alter_column('from_time',
               existing_type=sa.TIME(),
               type_=sa.Text(),
               existing_nullable=True)
        batch_op.alter_column('to_time',
               existing_type=sa.TIME(),
               type_=sa.Text(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('menu', schema=None) as batch_op:
        batch_op.alter_column('to_time',
               existing_type=sa.Text(),
               type_=sa.TIME(),
               existing_nullable=True)
        batch_op.alter_column('from_time',
               existing_type=sa.Text(),
               type_=sa.TIME(),
               existing_nullable=True)

    # ### end Alembic commands ###
