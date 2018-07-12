#!/bin/sh
echo Which repertory are you targeting ? Please enter 'IPMA' or 'ARTICLES'.
read repertory
echo What is the name of your filenames file ?
read name
targeted_directory=$repertory'/INPUTS/'
for i in $(ls "$targeted_directory")
do
	echo "$(realpath "$targeted_directory""$i")" >> $name
done

