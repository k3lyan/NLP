# Pipeline
A pipeline to preprocess given set of documents.

## Requirements
Download and install [Stanford Core NLp](https://stanfordnlp.github.io/CoreNLP/index.html#download) for French

Download and install [NERC-fr](https://github.com/opener-project/nerc-fr)

Download and install [TreeTagger](http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/) along with French parameter files

## Getting Started
First convert the documents into raw text using the [text extraction module](../ExtractText).

Update each shell scripts with the path of corresponding required application.

To extract POS and Dependancy Structure:

`runCoreNLPFrench.sh INPUT_FOLDER OUTPUT_FOLDER`

To extract Named Entities:

`runNERCfr.sh INPUT_FOLDER OUTPUT_FOLDER`

To extract Chunks and Lemmas:

`runTreeTagger.sh INPUT_FOLDER OUTPUT_FOLDER`
