"""empty message

Revision ID: 6756ae84b10c
Revises: 6ed892be7364
Create Date: 2022-06-17 15:46:58.795501

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6756ae84b10c'
down_revision = '6ed892be7364'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('gene_filtered', sa.Column('celltype', sa.String(), nullable=True))
    op.drop_index('index_gene_filter', table_name='gene_filtered')
    op.create_index('index_gene_filter', 'gene_filtered', ['gene', 'timepoint', 'celltype'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('index_gene_filter', table_name='gene_filtered')
    op.create_index('index_gene_filter', 'gene_filtered', ['gene', 'timepoint'], unique=False)
    op.drop_column('gene_filtered', 'celltype')
    # ### end Alembic commands ###