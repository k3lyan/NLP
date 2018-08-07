#!/bin/bash

stanfordCP= #Path where Stanford Core NLP is saved
inFolder=$1
outFolder=$2

find $1 -type f > myFileList.txt

java -Xmx54g -cp "$stanfordCP/*" edu.stanford.nlp.pipeline.StanfordCoreNLP -props StanfordCoreNLP-french.properties -annotators tokenize,ssplit,pos,depparse  -ssplit.newlineIsSentenceBreak always -filelist myFileList.txt -outputFormat conll -outputDirectory $2

rm myFileList.txt
