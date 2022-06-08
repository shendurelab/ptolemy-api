from sqlalchemy import String, Float, Integer, Column
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


def get_gene(model):
    # TODO: dynamically create gene filter columns list from user input
    gene_columns = {
        "timepoint": String
    }

    class gene(model):
        __tablename__ = 'gene'
        __table_args__ = {'extend_existing': True}
        id = Column(Integer, primary_key=True)
        gene = Column(String)
        data = Column(JSON)

    update_table(gene, gene_columns)
    return gene
