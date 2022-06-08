from app import app, gene, db
from app.schema import gene_schema
from app.utils import import_cells_handeler, import_genes_handeler
from flask import request
from timeit import default_timer as timer


@app.post('/genes')
def genes():
    # TODO: dynamically assign from user input
    t1 = timer()
    filter_columns = ["timepoint"]
    data = request.get_json()
    import_genes_handeler(db.session, data, filter_columns)
    t2 = timer()
    total_time = t2-t1
    print(total_time)
    return 'ok'


@app.post('/cells')
def cells():
    # TODO: dynamically assign from user input
    t1 = timer()
    filter_columns = ["timepoint"]
    data = request.get_json()
    import_cells_handeler(db.session, data)
    t2 = timer()
    total_time = t2-t1
    print(total_time)
    return 'ok'
