#!/bin/sh
echo Which repertory are you targeting in the DATA module? Please enter 'IPMA' or 'ARTICLES'.
read repertory
echo Which extension would you like to delete? example: txt
read extension
target='../DATA/'$repertory'/*.'$extension
for file in $target
do
	mv -- "$file" "${file%%.$extension}"
done

