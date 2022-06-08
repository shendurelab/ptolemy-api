"""empty message

Revision ID: 4c4f4afdd994
Revises: 74fd89d42ced
Create Date: 2022-06-03 12:52:24.939729

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4c4f4afdd994'
down_revision = '74fd89d42ced'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cell',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('major_trajectory', sa.String(), nullable=True),
    sa.Column('celltype', sa.String(), nullable=True),
    sa.Column('somite_stage', sa.String(), nullable=True),
    sa.Column('day', sa.String(), nullable=True),
    sa.Column('timepoint', sa.String(), nullable=True),
    sa.Column('UMAP_3d_1', sa.Float(), nullable=True),
    sa.Column('UMAP_3d_2', sa.Float(), nullable=True),
    sa.Column('UMAP_3d_3', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('gene',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('gene', sa.String(), nullable=True),
    sa.Column('data', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('timepoint', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('word')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('word',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('english', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('korean', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('romanian', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='word_pkey')
    )
    op.drop_table('gene')
    op.drop_table('cell')
    # ### end Alembic commands ###