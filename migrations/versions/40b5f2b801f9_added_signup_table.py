"""added signup table

Revision ID: 40b5f2b801f9
Revises: 45a49c554cd0
Create Date: 2024-02-26 21:22:26.695333

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40b5f2b801f9'
down_revision = '45a49c554cd0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('signup',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password_hash', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('signup')
    # ### end Alembic commands ###
