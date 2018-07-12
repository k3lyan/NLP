# clean_white_spaces.py 
## Input: 
Nothing, but be sure to have a directory 'IPMA' and 'ARTICLES', inside of each is contained a directory 'INPUTS' containing the files
## Output: 
Nothing, but all the titles of the files targeted have been changed, every white space has been substituted by '_'.
## Goal:
Delete all the white spaces in the titles (it's better without, for bash manipulations for example)
## How to use:
`$python3 clean_white_spaces.py` 

# filenames_builder.sh 
## Input:
Nothing, but be sure to have a directory 'IPMA' and 'ARTICLES', inside of each is contained a directory 'INPUTS' containing the files
## Output:
A file containing all the absolute path to the raw files, each line is a path.
## Goal:
Get a file of absolute pathes towards our data
## How to use:
`$./filenames_builder.sh`  
(Be sure to have at least the execution right for the bash script, one could type: $sudo chmod 777 filenames_builder.sh)
