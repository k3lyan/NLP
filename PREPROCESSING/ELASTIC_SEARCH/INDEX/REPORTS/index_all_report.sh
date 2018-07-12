#!/bin/sh
for i in `seq 0 172`;
do
	python3 report_indexing.py report_paths $i $i
done
