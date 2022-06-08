postgres:
	docker run -p 5433:5432 --name postgres-ptolemy -e POSTGRES_PASSWORD=secret -e POSTGRES_USER=root -d postgres:13-alpine

createdb:
	docker exec -it postgres-ptolemy createdb ptolemy

dropdb:
	docker exec -it postgres-ptolemy dropdb ptolemy

server:
	pipenv run flask run

migrateup:
	pipenv run flask db migrate && pipenv run flask db upgrade

-PHONY: postgres, createdb, dropdb

