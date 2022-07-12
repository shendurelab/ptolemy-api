import sqlalchemy
from app import app, db, cell
from app.utils import import_cells_handeler, import_genes_handeler
from flask import request
from timeit import default_timer as timer


@app.post('/genes')
def genes():
    t1 = timer()
    # TODO: dynamically assign from user input
    filter_columns = ["timepoint", "celltype"]
    filter_data = {}#{"timepoint":"E9"}
    data = request.get_json()
    import_genes_handeler(db.session, data["data"], filter_columns, filter_data)
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


@app.get('/gene_unfiltered')
def gene_unfiltered():
    params = request.args.to_dict()
    stmt = """
    select
      cell."UMAP_3d_1" as x,
      cell."UMAP_3d_2" as y,
      cell."UMAP_3d_3" as z,
      coalesce(g.value, 0 ::text) as expression
    from
      cell
      left join (
        select
          key,
          value
        from
          (
            select
              value as v
            from
              gene_unfiltered g,
              json_array_elements(g.data)
            where
            g.gene = :gene
          ) j,
          json_each_text(j.v)
      ) g on g.key = cell.id
    where
      timepoint = :timepoint
    order by
      timepoint
    """
    data = db.session.execute(sqlalchemy.text(stmt), params)
    response = [[c for c in data.keys()]]
    response.extend([[i for i in row] for row in data])
    return {"data":response}

@app.get('/gene_filtered')
def gene_filtered():
    t1 = timer()
    params = request.args.to_dict()
    stmt = """
    select
      cell."UMAP_3d_1" as x,
      cell."UMAP_3d_2" as y,
      cell."UMAP_3d_3" as z,
      coalesce(g.value, 0 ::text) as expression
    from
      cell
      left join (
        select
          key,
          value
        from
          (
            select
              value as v
            from
              gene_filtered g,
              json_array_elements(g.data)
            where
            g.gene = :gene
            and timepoint = :timepoint
          ) j,
          json_each_text(j.v)
      ) g on g.key = cell.id
    where
      timepoint = :timepoint
    order by
      timepoint
    limit 10000;
    """
    data = db.session.execute(sqlalchemy.text(stmt), params)
    response = [[c for c in data.keys()]]
    response.extend([[i for i in row] for row in data])
    t2 = timer()
    total_time = t2-t1
    print(total_time)
    return {"data":response}


@app.get('/cell')
def get_cell():
    t1 = timer()
    params = request.args.to_dict()

    stmt = f"""
    select
      cell."UMAP_3d_1" as x,
      cell."UMAP_3d_2" as y,
      cell."UMAP_3d_3" as z,
      cell.{params['annotation']}
    from
      cell
    where
      timepoint = :timepoint
    order by
      {params['annotation']}
    """

    data = db.session.execute(sqlalchemy.text(stmt), params)
    response = [[c for c in data.keys()]]
    response.extend([[i for i in row] for row in data])
    t2 = timer()
    total_time = t2-t1
    print(total_time)
    return {"data": response}

@app.get('/filter_option')
def filter_options():
    params = request.args.to_dict()
    if params['option'] not in [column.key for column in cell.__table__.columns]:
        return {"error": "option does not exist"}, 404
    
    stmt = f"""
    select {params['option']} from cell group by {params['option']}
    """
    data = db.session.execute(sqlalchemy.text(stmt), params)
    response = [x[0] for x in data]
    return {"options":response}


@app.get('/annotation_options')
def annotation_options():
    response = [column.key for column in cell.__table__.columns if column.key not in ['id', 'UMAP_3d_1', 'UMAP_3d_2', 'UMAP_3d_3']]
    return {"options":response}
