# WEB SCRAPING EXTRACTION
This module aims at extract text data from the web.

## WIKIPEDIA ARTICLES EXTRACTION 
### Input: 
Txt file containing in each line the title of a wikipedia article (in a same choosen language supported by the wikipedia api)

### Output: 
Txt files each of one containing a wikipedia article. They are located in the destination root directory (which must have been created)

### Goal: 
Get a specific list of txt articles from wikipedia in a specific language

### How to use:
Example:     
`$python3 extraction_articles articles_list language`

articles_list: the txt file containing the titles of the articles
language: the language supported by wikipediaapi in which the article are written (ex: fr, en, es,...)
destination_root: the directory where we'll be put the outputs, ex: '../DATA/ARTICLES'

### Libraries to install:
$pip3 install wikipedia-api


