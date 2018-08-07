#!/bin/sh
for i in `seq 0 47`;
do
	python3 ipma_indexing.py ipma_paths $i $i
done
