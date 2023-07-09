"""project migration2.

Revision ID: 36038c1facc4
Revises: 86d49fe64e6d
Create Date: 2023-07-09 19:28:34.020177

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36038c1facc4'
down_revision = '86d49fe64e6d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('linkage', schema=None) as batch_op:
        batch_op.add_column(sa.Column('presence', sa.Boolean(), nullable=True))

    with op.batch_alter_table('school', schema=None) as batch_op:
        batch_op.add_column(sa.Column('release_date', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('school', schema=None) as batch_op:
        batch_op.drop_column('release_date')

    with op.batch_alter_table('linkage', schema=None) as batch_op:
        batch_op.drop_column('presence')

    # ### end Alembic commands ###
