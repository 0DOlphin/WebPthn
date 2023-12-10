"""Renamed password column

Revision ID: af18e2426a1d
Revises: f3f3c578f08f
Create Date: 2023-11-04 23:23:25.466445

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af18e2426a1d'
down_revision = 'f3f3c578f08f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'password', new_column_name='password_hash')
    # with op.batch_alter_table('user', schema=None) as batch_op:
    #     batch_op.add_column(sa.Column('password_hash', sa.String(length=60), nullable=False))
    #     batch_op.drop_column('password')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.VARCHAR(length=60), nullable=False))
        batch_op.drop_column('password_hash')

    # ### end Alembic commands ###