# tokenizer_sentence.py 
## Input: 
sys.argv[1]: root directory containing all the inputs    
sys.argv[2]: root targeted directory     
## Output: 
Tokenized files in the same arborescence than the initial one except for the directory root that switched from sys.argv[1] value to sys.argv[2] value. 
## Goal: 
Tokenize raw texts:   
* each sentence represents one line of the tokeniozed file  
* each word of the sentence is seperated by 1 single whitespace  
## How to use:  
Example:    
`$python3 tokenize.py ./ARTICLES/ ./tokenized_articles/`  
Where:
* ./ARTICLES is the root repertory containig the articles txt files in its arborescence
* ./tokenized_articles is the destination root (will be automatically created if it doesn't exist yet), having the same arborescence than ./ARTICLES/ but where the txt files have been replaced by their tokenized version.      
## Libraries needed:
Install spacy:   
`$pip install -U spacy`
Download the French language model:   
`$pip -m spacy download fr`
Install textacy:      
`$pip install textacy`
