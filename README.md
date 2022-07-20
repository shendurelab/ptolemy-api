
# Ptolemy API

*A headless cell x gene UMAP visualization tool*

This project is the API for the second iteration of the mouse mutant cell atlas visualization (https://atlas.gs.washington.edu/mmca_v2/) using a different cell x gene dataset. This rebuild used upgraded libraries, tools, and abstractions to minimize the work needed to use different datasets in the future.

## Overview

Ptolemy API generates the database and serves requests to the corresponding Ptolemy front-end repo. It uses the Flask framework for the API service and a Postgres docker container.

## Install

1. This project uses `pipenv` for package management. Install `pipenv` if you do not have it installed already.

2. Install packages `pipenv install`

The recommended database setup is to use a Postgres docker image. Make sure you have docker installed. You may use your system's database if you like, just configure the correct URI in the `.env` file.

3. Install the Postgres docker image `docker pull postgres:13-alpine`

4. Create an instance of the image `make Postgres`

5. Create the database `make createdb`

6. Configure .env file by removing '.example' from the .example.env file.

7. Run migrations `make migrateup`

8. Start server `make server`

## Import

Once the server is running, the user must provide at least 2 datasets.

1. The cell x gene matrix with genes as rows, cells as columns, and values as expression.

> The project recommends the data be in a sparse matrix data struct and saved as an .rds file.

2. The cell's metadata. This will have cells as the rows and columns as the various attributes for the cells such as trajectories, mutations, or timepoints.

The next step is to put the files in the project's top directory and run:
```sh
./import_genes.sh cellxgene_file_name number_of_threads timepoint_value
```
Replace `cellxgene_file_name` with the file name of the .rds file containing the cellxgene matrix.

Replace `number_of_threads` with how many processes you want to split the import by. The server defaults to using 4 workers so that is the maximum unless you edit the `make server` command to run more workers.

>TODO: make `timepoint_value` optional and dynamic depending on the filters used

Replace `timepoint_value` with the value to use for the timepoint.
  

## Routes

#### POST `/genes` parameters

Populates the database with cell x gene data.

- `filter_columns`: list containing all columns the user intends to filter the data on. (temporarily disabled and defaulted to `["timepoint"]`)

- `filter_data`: dictionary to manually provide the data for the filter_columns. This will speed up the import process because it skips querying the values from the `cell` metadata

- `data`: dictionary with the key as the gene name and value as a list of dictionaries with the keys being "cell" and "expression"; and values being the cell id and expression number. See the example below:

```json
{
	"ENSMUSG00000061024":
	[
		{"cell":"run_15_PD-01E_S293.TATGAGAACTAGTAACGGTC",
	"expression":"1"},
		...
	]
}
```

> *Note*: If `filter_columns` is specified the data will be inserted in the `gene_filtered` table, however, if `filter_columns` is not specified, the data will be inserted in the `gene_unfiltered` table. This matters because it determines which of the below get requests to use. `filter_columns` is currently hard coded as `["timepoint"]`.

#### GET `/gene_filtered`

Returns the cells x, y, and z UMAP coordinates and the expression value for a specified gene from the `gene_filtered` table. Accepts the query params:

- `gene`: Name of the gene to show the expression for

> TODO: dynamically create filter query params. `timepoint` is hardcoded in this case.

- `timepoint`: Filters the results to the specified timepoint

Returns the results as a list of lists wrapped in a dictionary with the first list containing the column names and the following lists containing the values. Example:

```json
{
	"data":
	[
		['x', 'y', 'z', 'expression'],
		['1', '0.5', '1', '2'],
		...
	]
}
```

#### GET `/gene_unfiltered`

Alternate of `/gene_filtered` used for the `gene_unfiltered` table.

#### POST `/cells`

Accepts a request body as a list of dictionaries with the metadata columns as the keys and values respectively. Example:

```json
[
	{
		"cell_id": "321",
		"major_trajectory": "test",
		"celltype": "test",
		"somite_stage": "test",
		"day": "test",
		"timepoint": "E9",
		"UMAP_3d_1": "1",
		"UMAP_3d_2": "1",
		"UMAP_3d_3": "1"
	}
]
```

#### GET `/cell`

Returns the cell's x, y, and z UMAP coordinates along with an annotation value. Accepts the query params:

- `annotation`: Must be one of the columns in the cell's metadata

> TODO: dynamically create filter query params. `timepoint` is hardcoded in this case.

- `timepoint`: Filters the results to the specified timepoint

Returns the results as a list of lists wrapped in a dictionary with the first list containing the column names and the following lists containing the values. Example:

```json
{
	"data":
	[
		['x', 'y', 'z', 'major_trajectory'],
		['1', '0.5', '1', 'blood'],
		...
	]
}
```

#### GET `/filter_option`

Returns the unique values for a column in the cell table. This is used for the front end to display what options are available for the filter

- `option` a column in the cell table.

#### GET `/annotation_options`

Returns the columns in the cell table that can be used to annotate the UMAP coordinates. In other words, returns all columns in the cell table beside the UMAP coordinates and id columns.

