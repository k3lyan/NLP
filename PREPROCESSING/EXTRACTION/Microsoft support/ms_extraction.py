#!/usr/bin/env python
import tika
from tika import parser
import json
import os
import sys
import re
import langid

#sys.argv[1]: directory path where all the files are (not necessarly microsoft files)
#sys.argv[2]: directory where we will stock all the converted files 

# Extract text with apache tika function 
tika.TikaServerEndpoint="http://localhost:9998/"
# Ensure that apache tika is listening at the specified port
tika.TikaClientOnly = True

def extract_text(inputFilePath, xmlOutput=False):
    """Returns the text parsed by Apache Tika.
    Arguments:
        inputFilePath -- the file to be parsed
        xmlOutput -- if true the parsed file will be in XML format
    """
    try:
        parsed_file = parser.from_file(inputFilePath, xmlContent=xmlOutput)
        # output is a json file
        # metadata is in parsed_file['metadata']
        if 'content' not in parsed_file:
            return None,'not content'
        else:
            return parsed_file['content'],None
    except IOError :
        return None,'IOError'
    except UnicodeEncodeError:
        return None,'UnicodeEncodeError'

# Clean text functions
def line_cleaner(sentence):
    return re.sub(r"[\n]", r"", sentence)

def balise_cleaner(sentence):
    regexp_balise = r"<(c|t|b\|a)*[^>]+>"
    return re.sub(regexp_balise, r" ", sentence)

# Get only Microsoft files in the directories
def get_paths(paths_files, extension_to_extract):
    compt=0
    with open(paths_files, 'r') as paths:
        ms_paths = []
        for line, path in enumerate(paths.readlines()):
            extension = path.strip().split('/')[-1].split('.')[-1].replace(' ','').lower() 
            if (extension in extension_to_extract):
                ms_paths.append('.'+line_cleaner(path))
                compt+=1
        paths.close()
    print("There are {} microsoft found".format(compt))
    return ms_paths

def path_generator(input_directory, extension_to_extract):
    compt=0
    paths = []
    microsoft_paths=[]
    for root, dirs, files in os.walk(input_directory, topdown=False):
        for name in files:                              
            paths.append(os.path.join(root, name))              
            for name in dirs:
                paths.append(os.path.join(root, name))
    for line, path in enumerate(paths):
    # KEEP ONLY MICROSOFT PATHS
        extension=path.strip().split('/')[-1].split('.')[-1].replace(' ','').lower() 
        if (extension in extension_to_extract):
            microsoft_paths.append(line_cleaner(path))
            compt+=1 
    print("There are {} microsoft found".format(compt))
    return microsoft_paths

# EXTRACT ALL MICROSOFRT CONTENT INTO TXT IN A NEW STRUCTURE
extension_to_extract=['pptx','ppt','xlsx','xls','docx','dox']
input_directory=sys.argv[1]
output_directory=sys.argv[2]
initial_path=path_generator(input_directory,extension_to_extract)
compteur=0

for rank, pdf_path in enumerate(initial_path):
    compteur+=1
    if((compteur%100)==0):
        print('---------------------')
        print("iter {}, fichier : {}".format(compteur,pdf_path))
        print('---------------------')

    # Change path 
    if not os.path.exists(output_directory):
        os.makedirs(destination_root)
    cleant_path = pdf_path.replace(' ', '_') 
    new_path = cleant_path.replace(input_directory, output_directory)  

    repertoire = '/'.join(new_path.split('/')[:-1])
    name=new_path.split('/')[-1]
    name_list=name.split('.')
    for ext in extension_to_extract:
        name_list[-1]=name_list[-1].lower().replace(ext,ext+'.txt')
    title='.'.join(name_list)

    # Get text of the document
    cleaned_file,reason=extract_text(pdf_path)
    if(cleaned_file!=None):
        language_txt=langid.classify(cleaned_file)[0]
        # Write in a analogue arboresence if not and english text
        if(language_txt=='fr'):
            # OR STOCK TXT FILES
            directory = repertoire.split('/')
            for d in range(1, len(directory)):
                directory[d] = '/'.join([directory[d-1], directory[d]])
                if not os.path.exists(directory[d]):
                    os.makedirs(directory[d])
            print('{}/{}'.format(repertoire, title))
            with open ('{}/{}'.format(repertoire, title), 'w')as outfile:
                outfile.write(cleaned_file)
                outfile.close()
'''     else:
            with open('./microsoft_files_other_language.tsv', 'a') as outfile:
                outfile.write("{}\t{}\n".format(pdf_path, language_txt))
                outfile.close()

    else :
            print('microsoft_corrupted')
            with open('./microsoft_files_corrupted.tsv', 'a') as outfile:
                outfile.write("{}\t{}\n".format(pdf_path,reason))
                outfile.close()'''


