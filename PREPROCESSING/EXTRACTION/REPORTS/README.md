## wrapper_pdf.py
A module enabling to parse an input pdf file with pdfminer.six library.

## extraction.py 
### Input 
A pdf file
### Output 
A raw text file, containing the text from PDF without bottom pages, what is before summary and appendix
### Goal 
Get the raw text content from a pdf file without useless information such as the bottom page, what is before the summary and what is in the appendix
### How to use
Add 4 repertories before executing the python script: 'english', 'sommaire', 'bas', 'annexe'  
`$python3 extraction.py pdf_file.pdf`

## pdf_to_text.sh 
### Input 
pdf files
### Output 
raw text files
### Goal 
execute extraction.py on several pdf files 
### How to use
Put this script in the same repertory than extraction.py, wrapper_pdf.py the pdf files and the 4 repertories.  
Launch on a terminal open in this main directory:  
`./pdf_to_text.sh`
### Libraries
`$pip install langid`  
`$pip install pdfminer.six`
