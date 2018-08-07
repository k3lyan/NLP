#!/bin/bash

inFolder=$1
outFolder=$2

nerModel= #Path to nerc-fr.bin file
nercFr= #Path to opennlp command in nerc-fr directory

find $inFolder -type f -printf "%p\n" | while read -d $'\n' file
do
	fileName=${file##*/}
	cat "$file" | $nercFr TokenNameFinder $nerModel > "$outFolder/$fileName"
done
