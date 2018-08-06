#!/bin/sh
targeted_directory='./meta_mails/'
for i in $(ls "$targeted_directory")
do
	echo "$(realpath "$targeted_directory""$i")" >> metamail_paths
done

