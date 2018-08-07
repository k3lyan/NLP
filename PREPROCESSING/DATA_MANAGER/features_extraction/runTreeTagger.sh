#!/bin/bash

inFolder=$1
outFolder=$2

frenchChunker= #Path to tagger-chunker-french

find $inFolder -type f -printf "%p\n" | while read -d $'\n' file
do
	fileName=${file##*/}
	cat "$file" | $frenchChunker > "$outFolder/$fileName"
done
