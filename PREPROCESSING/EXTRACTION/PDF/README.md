# PDF EXTRACTION
This module aims at extracting PDF files into raw text files. The library pdfminer.six is used.

## pdfminer.six
* PDF parser and analyzer
* Fork of PDFMiner using six for Python 2+3 compatibility.
* PDFMiner is a tool for extracting information from PDF documents. Unlike other PDF-related tools, it focuses entirely on getting and analyzing text data. PDFMiner allows to obtain the exact location of texts in a page, as well as other information such as fonts or lines. It includes a PDF converter that can transform PDF files into other text formats (such as HTML). It has an extensible PDF parser that can be used for other purposes instead of text analysis.

## Installation
 * Install Python 2.7 or newer. (Python 3.x is supported in pdfminer.six)
 * Install with pip:
    $ pip install pdfminer.six
 * Install with conda:
    $ conda install -c conda-forge pdfminer.six

# PDF FULL EXTRACTION
## wrapper_pdf.py 
A module enabling to parse an input pdf file with pdfminer.six library.

## extraction_pdf.py 
### Input: 
* sys.argv[1]: Source directory root, a directory containing PDF files in its subdirectories
* sys.argv[2]: Destination directory root, the directory from where will be duplicate the arborescence of the source directory root, but where PDF file will have been converted into TXT files.
### Output: 
A bunch of directories corresponding to the substructure of the source directory root, where PDF have been extracted.
### Goal: 
Extract and convert into TXT files all PDF files of an arborescence.
### How to use:
Launch in a terminal:     
`$python3 extraction_pdf.py initial_root destination_root`

# PDF REPORTS EXTRACTION
## wrapper_pdf.py 
A module enabling to parse an input pdf file with pdfminer.six library.

## extraction_reports.py 
### Input: 
A pdf file
### Output: 
A raw text file, containing the text from PDF without bottom pages, what is before summary and appendix
### Goal: 
Get the raw text content from a pdf file without useless information such as the bottom page, what is before the summary and what is in the appendix
### How to use:
Add 4 repertories before executing the python script: 'english', 'sommaire', 'bas', 'annexe' then lauch in a terminal:     
`$python3 extraction_reports.py pdf_file.pdf`

## pdf_reports_to_text.sh 
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
