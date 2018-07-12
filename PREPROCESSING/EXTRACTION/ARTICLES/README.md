## WIKIPEDIA ARTICLES EXTRACTION 
### Input: 
Txt file containing in each line the title of a wikipedia article (in a same choosen language supported by the wikipedia api)
### Output: 
Txt files each of one containing a wikipedia article. They are located in they INPUTS/ repertory (which must have been created)
### Goal: 
Get a specific list of txt articles from wikipedia in a specific language
### How to use:
`$python extraction_articles list_titles_file language`  
list_title_file: the txt file containing the titles of the articles  
language: the language supported by wikipediaapi in which the article are written (ex: fr, en, es,...)
### Libraries to install:
`$pip install wikipedia-api`
