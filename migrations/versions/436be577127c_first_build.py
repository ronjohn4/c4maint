"""first build

Revision ID: 436be577127c
Revises: 
Create Date: 2020-03-07 09:56:03.231821

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '436be577127c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('parent',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('sex', sa.Integer(), nullable=True),
    sa.Column('dob', sa.Date(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('income_amount', sa.Numeric(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('parent_audit',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('a_datetime', sa.DateTime(), nullable=True),
    sa.Column('action', sa.String(length=64), nullable=True),
    sa.Column('before', sa.String(), nullable=True),
    sa.Column('after', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['parent_id'], ['parent.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('parent_audit')
    op.drop_table('parent')
    # ### end Alembic commands ###
