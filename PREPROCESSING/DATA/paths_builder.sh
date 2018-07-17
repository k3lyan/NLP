#!/bin/sh
echo what is the name of the targeted directory ?
read directory
echo What is the name of your filenames file ?
read name
targeted_directory='./'$directory'/'
echo "$targeted_directory"
for i in $(ls "$targeted_directory")
do
	echo "$(realpath "$targeted_directory""$i")" >> $name
done

