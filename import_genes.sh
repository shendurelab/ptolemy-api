#!/bin/bash

threads=$2

for ((i=1; i<=threads; i++))
do
	./rds_import.R $1 $threads $i $3 &
done

