# jax-mouse

3d umap vizualization with filtering accross hundreds of millions of datapoints.

## install
1. `pipenv install`
2. `make postgres`
You can edit the db password in the makefile, just make sure to update your .env file too
3. `make createdb`
4. `make migrateup`

## Run
`make server`
