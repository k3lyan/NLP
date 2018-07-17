#!/bin/sh
echo What is the name of your filenames file ?
read name
targeted_directory='./REPORTS/'
echo "$targeted_directory"
for i in $(ls "$targeted_directory")
do
	echo "$(realpath "$targeted_directory""$i")" >> $name
done

