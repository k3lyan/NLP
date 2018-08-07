# DUPLICATE DETECTION
This module aims at detect duplicate, eliminate them while keeping a track of it.

## hash.py
### Input:
* sys.argv[1]: the targeted root dirtectory
### Output: 
* 'unique_files': File containing the path of the unique files, one path per line.
* 'duplicate_files': File containing for each line the path of the unique file: the paths of the duplicates.    
ex: path/to/the/unique/file/unique_file.txt: path/to/duplicate/duplicate1.txt, path/to/another/duplicate2.txt 
### Goal:
Detect, suppress but keep track of all the duplicate file in a root directory and all its subdirectories. Files are sorted depending on their SHA256 hash and their size. Files with the same hash are considered duplicates.
### How to use it:
`python3 hash.py targeted_root_directory`

