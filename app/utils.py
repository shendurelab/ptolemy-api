from app import cell, gene_filtered, gene_unfiltered
from sqlalchemy.orm.session import Session


def import_genes_handeler(
        session: Session, 
        gene_data, 
        filter_columns: list[str] = [],
        filter_data: dict[str, str] = {}):
    '''
    Populate the `gene` table with a dict from api call.

    Accepts gene_data as type dict["<gene>", list[dict["cell": "<cell_id>",
        "expression": <expression number>]]]
    The filter_columns param is a list[str] that contains all columns that
    will be used for filtering gene expressions.

    Optionally: you may provide filter_data to manually provide the data for
    the filter_columns. This will speed up the import because it skips querying
    the values from the cell table. This should be used if all cells in the
    import have the same data for their filter_columns. This variable should be
    formatted with {"column_name":"value"}. When this variable is provided,
    filter_columns will be disregarded.

    benchmark for None filter_data: 
    16,034 non-0 gene expressions accross 2 genes in 11.1 sec
    - 300,000,000 entries in 57 hours
    67,487 entries in 45.5 sec
    - 300,000,000 entries in 56 hours  

    benchmark with filter_data:
    293,240 entries in 1.09 sec
    - 300,000,000 entries in 18 min (yay!)  
    '''
    for gene_label, cell_expressions in gene_data.items():

        # dict of gene objects to upload to the db. key is concatination of
        # filter values for quick check if exists and access
        gene_rows = {}

        filter_group = filter_data
        filter_group_key = "".join(filter_group.values()) if filter_data else "a"

        for item in cell_expressions:
            expression_dict = {item['cell']: item['expression']}

            if filter_columns and not filter_data:
                # cell's metadata for each filter_column specifcied by user
                c = session.query(cell).filter_by(id=item["cell"]).first()
                if c is None:
                    print(f'{item["cell"]} could not be found in table `cell`')
                    continue
                filter_group = {col: getattr(c, col) for col in filter_columns}
                filter_group_key = "".join(filter_group.values())

            if filter_group_key not in gene_rows:
                if not filter_columns and not filter_data:
                    g = gene_unfiltered(gene=gene_label, data=[
                             expression_dict])
                else:
                    g = gene_filtered(gene=gene_label, data=[
                             expression_dict], **filter_group)
                gene_rows[filter_group_key] = g
            else:
                gene_rows[filter_group_key].data.append(expression_dict)

        session.bulk_save_objects(gene_rows.values())
    session.commit()


def import_cells_handeler(session, cells):
    '''
    Populate the `cell` table with list of dicts from api call
    accepts cells: List[Dict{"cell_id": String ...}]
    benchmark: 200,000,000 cells in 19.6 sec
    '''

    for cell_row in cells:
        # TODO: dynamically create cell from existing columns
        c = cell(id=cell_row['cell_id'],
                 major_trajectory=cell_row['major_trajectory'],
                 celltype=cell_row['celltype'],
                 somite_stage=cell_row['somite_stage'],
                 day=cell_row['day'],
                 timepoint=cell_row['timepoint'],
                 UMAP_3d_1=cell_row['UMAP_3d_1'],
                 UMAP_3d_2=cell_row['UMAP_3d_2'],
                 UMAP_3d_3=cell_row['UMAP_3d_3'],
                 )
        session.add(c)
    session.commit()
