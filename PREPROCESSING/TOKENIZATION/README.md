# RAW TXT TO TOKENIZED SENTENCES 
## Input: 
File listing the titles of all files to be tokenized.  
This file can be produced using filenames_builder.sh in the repertory DATA/.  
## Output: 
Tokenized files in the repertory "OUTPUTS". 
See 'how to use' section for more details.
## Goal: 
Tokenizing raw texts:   
* each sentence represents one line of the tokeniozed file  
* each word of the sentence is seperated by 1 single whitespace  
## How to use:  
* 1st argument: path to the file containing all the files title --> to get the list of titles, please use clean_white_spaces.py and filenames_builder.sh in the directory 'DATA/' on the AI github
* you need to have 3 repertories 'ARTICLES', 'IPMA', 'TEST' ('REPORT' hasn't been kept due to privacy terms conditions)
* In each of these repertories you need to have a repertory called 'OUTPUTS', the results will be stocked there  
example:    
`$python3 txt_to_sents_words.py raw_report_titles`  
## Libraries needed:
Install spacy:   
`$pip install -U spacy`    
Download the French language model:    
`$pip -m spacy download fr`  
Install textacy:        
`$pip install textacy`
