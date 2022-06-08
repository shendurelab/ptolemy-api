from app import cell, gene


def import_genes_handeler(session, gene_data, filter_columns):
    '''
    Populate the `gene` table with a dict from api call
    accepts a gene_data: Dict{"gene":List[Dict{"cell": String, "expression": Int}]}
    benchmark: 16,034 non-0 gene expressions accross 2 genes in 11.1 sec
    - 300,000,000 genes 57 hours
    '''
    for gene_label, cell_expressions in gene_data.items():

        genes = {}

        for item in cell_expressions:
            expression_dict = {item['cell']: item['expression']}

            # cell's metadata for each filter specifcied by user
            c = session.query(cell).filter_by(id=item["cell"]).first()
            if c is None:
                print(f'{item["cell"]} could not be found in table `cell`')
                continue
            filter_group = {col: getattr(c, col) for col in filter_columns}
            filter_group_key = "".join(filter_group.values())

            if filter_group_key not in genes:
                g = gene(gene=gene_label, data=[
                         expression_dict], **filter_group)
                genes[filter_group_key] = g
            else:
                genes[filter_group_key].data.append(expression_dict)

        session.bulk_save_objects(genes.values())
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
