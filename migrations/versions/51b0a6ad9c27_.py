"""added phone, address, extra to OrderDetail

Revision ID: 51b0a6ad9c27
Revises: 21318fd3842f
Create Date: 2023-11-19 22:04:38.989446

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '51b0a6ad9c27'
down_revision = '21318fd3842f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order_detail', schema=None) as batch_op:
        batch_op.add_column(sa.Column('phone', sa.String(length=12), nullable=True))
        batch_op.add_column(sa.Column('address', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('extra', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order_detail', schema=None) as batch_op:
        batch_op.drop_column('extra')
        batch_op.drop_column('address')
        batch_op.drop_column('phone')

    # ### end Alembic commands ###
