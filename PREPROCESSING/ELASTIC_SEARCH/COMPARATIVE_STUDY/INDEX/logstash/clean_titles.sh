#!/bin/sh

echo Which extension would you like to delete? example: txt
read extension

for file in ./IPMA/*.$extension
do
	mv -- "$file" "${file%%.$extension}"
done

