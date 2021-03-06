"""empty message

Revision ID: c8161cd56b29
Revises: None
Create Date: 2016-07-02 13:47:25.142790

"""

# revision identifiers, used by Alembic.
revision = 'c8161cd56b29'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('listings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('company', sa.String(length=32), nullable=True),
    sa.Column('title', sa.String(length=128), nullable=True),
    sa.Column('status', sa.String(length=10), nullable=True),
    sa.Column('scraped_dt', sa.DateTime(), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('listings')
    ### end Alembic commands ###
