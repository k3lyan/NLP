# EXTRACTION
This module aims at extract all types of digital sources containing text data to raw text files.
* PDF extraction
* Microsoft office
* Web scraping 

# PDF EXTRACTION
See the directory PDF.

# MICROSOFT FILES EXTRACTION
See the directory MS.

# WIKIPEDIA ARTICLES EXTRACTION 
## Input: 
Txt file containing in each line the title of a wikipedia article (in a same choosen language supported by the wikipedia api)

## Output: 
Txt files each of one containing a wikipedia article. They are located in the destination root directory (which must have been created)

## Goal: 
Get a specific list of txt articles from wikipedia in a specific language

## How to use:
Example:     
`$python3 extraction_articles articles_list language`

articles_list: the txt file containing the titles of the articles
language: the language supported by wikipediaapi in which the article are written (ex: fr, en, es,...)
destination_root: the directory where we'll be put the outputs, ex: '../DATA/ARTICLES'

## Libraries to install:
$pip3 install wikipedia-api

# PDF REPORTS EXTRACTION
## wrapper_pdf.py ###
A module enabling to parse an input pdf file with pdfminer.six library.

## extraction.py ###
### Input: 
A pdf file
### Output: 
A raw text file, containing the text from PDF without bottom pages, what is before summary and appendix
### Goal: 
Get the raw text content from a pdf file without useless information such as the bottom page, what is before the summary and what is in the appendix
### How to use:
Add 4 repertories before executing the python script: 'english', 'sommaire', 'bas', 'annexe' then lauch in a terminal:     
`$python3 extraction.py pdf_file.pdf`

## pdf_reports_to_text.sh ###
### Input: 
pdf files
### Output: 
raw text files
### Goal: 
execute extraction.py on several pdf files 
### How to use:
Put this script in the same repertory than extraction.py, wrapper_pdf.py the pdf files and the 4 repertories.           
Launch on a terminal open in this main directory:
`./pdf_to_text.sh`
