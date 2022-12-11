"""Added invoice

Revision ID: bff34a64da66
Revises: 52286a2f8cdb
Create Date: 2022-12-11 15:23:36.290294

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bff34a64da66'
down_revision = '52286a2f8cdb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('invoice',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('invoice_belopp', sa.Integer(), nullable=False),
    sa.Column('forfallodatum', sa.Date(), nullable=False),
    sa.Column('betald', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('booking', schema=None) as batch_op:
        batch_op.add_column(sa.Column('invoice_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'invoice', ['invoice_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('booking', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('invoice_id')

    op.drop_table('invoice')
    # ### end Alembic commands ###