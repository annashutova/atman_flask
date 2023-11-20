"""added phone, replaced first_name and last_name with name

Revision ID: 21318fd3842f
Revises: 38f56b1ecfd5
Create Date: 2023-11-19 21:45:13.428022

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21318fd3842f'
down_revision = '38f56b1ecfd5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('phone', sa.String(length=12), nullable=True))
        batch_op.drop_column('last_name')
        batch_op.drop_column('first_name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('first_name', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('last_name', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
        batch_op.drop_column('phone')
        batch_op.drop_column('name')

    # ### end Alembic commands ###
