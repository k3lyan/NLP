# RISKS DETECTIONS
Get a file listing risks from the risk register (xlsx files). 

## Indexing emails (MAILS)
### Input:
* 'mail_paths': a txt file containing the absolute paths to the mails
### Outputs:
* 'mails.json': the JSON file containing all the indexing requests to Elasticsearch
### How to use:
Run in a terminal opened at the directory containing the files:                      
`$python3 mail_indexing.py mails_paths`                         
Then, while Elasticsearch is running on the localhost:                        
`$curl -H "Content-Type:application/json" -XPOST "http://localhost:9200/hydro_mail/mail/_bulk?pretty" --data-binary "@mails.json"`                           

## Indexing headers (HEADERS) 
### Input:
* 'header_paths', a txt file containing the absolute paths to the headers
### Outputs:
* 'headers.json': the JSON file containing all the indexing requests to Elasticsearch
### How to use:
Run in a terminal opened at the directory containing the files:                              
`$python3 header_indexing.py headers_paths`                                  
Then, while Elasticsearch is running on the localhost:                                
`$curl -H "Content-Type:application/json" -XPOST "http://localhost:9200/hydro_head/header/_bulk?pretty" --data-binary "@headers.json"`                 

## Indexing metamails (METAMAILS)
### Preparation of the inputs 
Creates a folder 'meta_mails' containing all the emails linked to a header (=metamails) and a file 'metamail_paths' containing the absolute paths to all these files
#### How to use:
`$python3 metamail_folder_builder.py'                 
### Indexing the metamails
#### Inputs:  
* 'header_paths' : a txt file containing the absolute paths to the headers
* 'metamail_paths' : a txt file containing the absolute paths to the metamails
#### Outputs:
* 'metamail.json': the JSON file containing all the indexing requests to Elasticsearch
### How to use:
`$python3 general_indexing.py metamail_paths header_paths`
