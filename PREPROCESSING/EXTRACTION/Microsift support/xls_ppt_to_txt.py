#!/usr/bin/env python
import tika
from tika import parser
import json
import os
import sys
import re
import langid

# Here is the code to convert document to txt APACHE TIKA


## APACHE TIKA ALLOWS TO EXTRACT PDF XLS PPT  DOCX ... ##


#### EXPLANATION ABOUT HOW TO DOWNLOAD APPACHE TIKA ###
'''
On extrait les documents docx avec Appache Tika telechargeable de la facon suivante :
A module to extract raw text from any document format (PDF, Microsoft Office etc.)

Requirements
Download Apache Tika here

Download Java ImageIO plugin for JBIG2 here (Source Code)

Download JAI Image I/O Tools Core

Download JPEG2000 support for Java Advanced Imaging Image I/O Tools API core from bintray

Install tika-python (Source Code)

pip install tika

Getting Started
Start the Apache Tika server and make sure that the jar files are in the classpath. For example,

java -cp "./*" org.apache.tika.server.TikaServerCli

will start the server at 9998 (default port) with the above mentioned jar files in the current directory.
'''

# INFORMATION INPUTS 
#sys.argv[1]: directory path where all the files are (not necessarly microsoft files)
#sys.argv[2]: directory where we will stock all the converted files 
##

# Extract text with apache tika function 
tika.TikaServerEndpoint="http://localhost:9998/"
#ensure that apache tika is listening at the specified port
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
##


# Cleaning titles and detecting language
def line_cleaner(sentence):
    return re.sub(r"[\n]", r"", sentence)

def balise_cleaner(sentence):
    regexp_balise = r"<(c|t|b\|a)*[^>]+>"
    return re.sub(regexp_balise, r" ", sentence)

# Get only microsoft files
def get_paths(paths_files,extension_to_extract):
    compt=0
    with open(paths_files, 'r') as paths:
        pdf_paths = []
        for line, path in enumerate(paths.readlines()):
            # KEEP ONLY PDF PATHS
            extension=path.strip().split('/')[-1].split('.')[-1].replace(' ','').lower() 
            if (extension in extension_to_extract):
                # ORIGINAL PATHS TO GET THE DATA -> '\ ' FOR CMD LINE
                #cmd_line_path = path.replace(' ', '\ ')
                pdf_paths.append('.'+line_cleaner(path))
                # print('DOCX_FOUND: {}'.format(path))
                compt+=1
        paths.close()
    print("There are {} microsoft found".format(compt))
    return pdf_paths

def path_generator(input_directory,extension_to_extract):
    compt=0
    paths = []
    microsoft_paths=[]
    for root, dirs, files in os.walk(input_directory, topdown=False):
        for name in files:                              
            paths.append(os.path.join(root, name))              
            for name in dirs:
                paths.append(os.path.join(root, name))
    for line, path in enumerate(paths):
    # KEEP ONLY MICROSOFT PAThS
        extension=path.strip().split('/')[-1].split('.')[-1].replace(' ','').lower() 
        if (extension in extension_to_extract):
            # ORIGINAL PATHS TO GET THE DATA -> '\ ' FOR CMD LINE
            microsoft_paths.append(line_cleaner(path))
            compt+=1 
    print("There are {} microsoft found".format(compt))
    return microsoft_paths
# EXTRACT ALL MICROSOFRT CONTENT INTO TXT IN A NEW STRUCTURE


#


## Variables

extension_to_extract=['pptx','ppt','xlsx','xls','docx','dox']
input_directory=sys.argv[1]
output_directory=sys.argv[2]
initial_path=path_generator(input_directory,extension_to_extract)
compteur=0
##

## MAIN

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


