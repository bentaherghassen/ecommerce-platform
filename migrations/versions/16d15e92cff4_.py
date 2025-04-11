"""empty message

Revision ID: 16d15e92cff4
Revises: e01c07cdfe57
Create Date: 2025-04-07 21:15:22.902408

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16d15e92cff4'
down_revision = 'e01c07cdfe57'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_added', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('author', sa.String(length=100), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.drop_column('author')
        batch_op.drop_column('date_added')

    # ### end Alembic commands ###
