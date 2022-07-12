from sqlalchemy import String, Float, Integer, Column, Index
from sqlalchemy.dialects.postgresql import JSON


def update_table(table, columns):
    for col, type in columns.items():
        setattr(table, col, Column(type))


def get_cell(model):
    # TODO: dynamically create columns list from cell metadata
    cell_columns = {
        "major_trajectory": String,
        "celltype": String,
        "somite_stage": String,
        "day": String,
        "timepoint": String,
        "UMAP_3d_1": Float,
        "UMAP_3d_2": Float,
        "UMAP_3d_3": Float,
    }

    class cell(model):
        __tablename__ = 'cell'
        __table_args__ = {'extend_existing': True}
        id = Column(String, primary_key=True)

    update_table(cell, cell_columns)
    return cell

def get_gene_unfiltered(model):
    # TODO: dynamically create gene filter columns list from user input

    class gene_unfiltered(model):
        __tablename__ = 'gene_unfiltered'
        gene = Column(String, primary_key=True)
        data = Column(JSON)

    return gene_unfiltered

def get_gene_filtered(model):
    # TODO: dynamically create gene filter columns list from user input
    gene_columns = {
        "timepoint": String,
        "celltype": String
    }

    class gene_filtered(model):
        __tablename__ = 'gene_filtered'
        id = Column(Integer, primary_key=True)
        gene = Column(String)
        data = Column(JSON)

    update_table(gene_filtered, gene_columns)
    Index('index_gene_filter', gene_filtered.gene, *[getattr(gene_filtered, c) for c in gene_columns.keys()])

    return gene_filtered
