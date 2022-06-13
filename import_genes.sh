#!/bin/bash

threads=4

for ((i=1; i<=threads; i++))
do
	./rds_import.R JAX_E9_count.rds $threads $i &
done
