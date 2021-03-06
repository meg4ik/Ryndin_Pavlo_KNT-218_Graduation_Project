"""user delete

Revision ID: 12c99d5687be
Revises: 5e3fc770fa8e
Create Date: 2022-01-09 20:08:38.732922

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12c99d5687be'
down_revision = '5e3fc770fa8e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('game', sa.Column('is_delete', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('game', 'is_delete')
    # ### end Alembic commands ###
