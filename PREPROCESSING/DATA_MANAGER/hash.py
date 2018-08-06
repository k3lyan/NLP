import hashlib
import sys
import re
import os
from collections import defaultdict

# GET FILE TUPLE: (path, hash, size)
def get_file_tuple(path):
    """Calculates the hash value for a file."""
    hash_object = hashlib.sha256()
    file_size = os.path.getsize(path)
    with open(path, 'r') as inputfile:
        #for chunk in iter(lambda:inputfile.read(1024 * 8), ""):
        hash_object.update(inputfile.read().encode())
        inputfile.close()
    return (path, (hash_object.hexdigest(), file_size))


#print(get_file_tuple(sys.argv[1]))
#print(get_file_tuple(sys.argv[1])[0])
#print(get_file_tuple(sys.argv[1])[1])

# GENERATE THE LIST OF EXTRACTED TEXT PATHS
def txt_generator(targeted_root):
    txt_paths = []
    for root, dirs, files in os.walk(targeted_root):
        for name in files:
            txt_paths.append(os.path.join(root, name))
    return txt_paths

def getkey(item):
    return item[1][0]

# SORT THE FILES TUPLES 
def sort_tuples(paths):
    tuples = []
    for p, path in enumerate(paths):
        tuples.append(get_file_tuple(path))
    return sorted(tuples, key=getkey)

def duplicated_files(tuples):
    dup = defaultdict(list) 
    unique = [tuples[0][0]]
    i = 0
    elem = tuples[0][0]
    while (i < len(tuples) - 1):
        if(tuples[i][1] == tuples[i+1][1]):
            dup[elem].append(tuples[i+1][0])
        else:
            elem = tuples[i+1][0]
            unique.append(elem)
        i += 1
    return (unique, dup)        

infos = duplicated_files(sort_tuples(txt_generator(sys.argv[1]))) 
unique_files = infos[0]
duplicated = dict(infos[1])
#print(unique_files)
#print(duplicated.keys())

with open('./unique_files', 'w') as unique:
    for i, name in enumerate(unique_files):
        unique.write('{}\n'.format(name))
    unique.close()

with open('./duplicate_files', 'w') as duplicate:
    for i in duplicated:
        #print('{}: {}\n'.format(i, duplicated[i]))
        duplicate.write('{}: {}\n'.format(i, duplicated[i]))
    duplicate.close()
