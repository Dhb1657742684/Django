"""empty message

Revision ID: 046b2416bc51
Revises: 
Create Date: 2019-09-29 11:58:39.121275

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '046b2416bc51'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('curriculum',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('c_id', sa.String(length=32), nullable=True),
    sa.Column('c_name', sa.String(length=32), nullable=True),
    sa.Column('c_time', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('leave',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('leave_id', sa.Integer(), nullable=True),
    sa.Column('leave_name', sa.String(length=32), nullable=True),
    sa.Column('leave_type', sa.String(length=32), nullable=True),
    sa.Column('leave_start', sa.String(length=32), nullable=True),
    sa.Column('leave_end', sa.String(length=32), nullable=True),
    sa.Column('leave_desc', sa.Text(), nullable=True),
    sa.Column('leave_phone', sa.String(length=32), nullable=True),
    sa.Column('leave_status', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=32), nullable=True),
    sa.Column('email', sa.String(length=32), nullable=True),
    sa.Column('password', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('leave')
    op.drop_table('curriculum')
    # ### end Alembic commands ###
