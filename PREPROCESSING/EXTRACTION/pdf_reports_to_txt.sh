#!/bin/sh
for i in *.pdf
do
  python extraction.py "$i"
done
