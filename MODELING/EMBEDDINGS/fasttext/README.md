## FASTTEXT EMBEDDINGS FOR COSINE SIMILARITY CALCULATIONS 
### Inputs:
Nothing. But be sure that the raw_files_titles listing the absolute pathes to the documents are here. 
For example, if you are trying to score skills in articles (my example), you should be sure that 'PM_paths.txt' and 'IPMA_paths.txt' files are in the directory.
### Outputs:
A .csv file containing the skills scores for each articles.    
### Goal:
Get cosine similarity scores using fasttext embeddings.
### How to use:
* Extract the fasttext model cc.fr.300.bin.gz, which enables to build word embeddings (French model).    
* In our example, we took articles and skills files to compare them. The pathes to these doc is written in the files 'raw_articles_titles' and 'raw_ipma_titles'. Feel free to update it.
`$python3 fasttext_embed.py`
### Libraries
You need to install pyfasttext.   
`$pip install pyfasttext`
