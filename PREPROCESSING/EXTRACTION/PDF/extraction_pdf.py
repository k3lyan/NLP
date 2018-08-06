from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LTTextBox, LTChar, LTTextLine
from wrapper_pdf import PdfMinerWrapper
import sys
import os
import re
import langid
from langid.langid import LanguageIdentifier, model
import random
from random import uniform

#sys.argv[1]: root directory containing all the inputs
#sys.argv[2]: root targeted directory

# CLEANING AND ANALYTICAL FUNCTIONS
def language_detect(text,identifier):
    identifier.set_languages(['fr','en'])
    return identifier.classify(text)

def line_cleaner(sentence):
    return re.sub(r"[\n]", r"", sentence)

def balise_cleaner(sentence):
    regexp_balise = r"<(c|t|b\|a)*[^>]+>"
    return re.sub(regexp_balise, r" ", sentence)

# GENERATE THE LIST OF ALL PDF SOURCES PATHS
def path_generator(path_sources):
    paths = []
    pdf_paths = []
    for root, dirs, files in os.walk(path_sources):
        for name in files:
            paths.append(os.path.join(root, name))
        for name in dirs:
            paths.append(os.path.join(root, name))
    for line, path in enumerate(paths):
        # KEEP ONLY PDF PATHS
        if (path.strip().split('/')[-1].split('.')[-1].replace(' ','').lower() == 'pdf'):
            pdf_paths.append(line_cleaner(path))
    return pdf_paths

#path_generator(sys.argv[1])

# FUNCTION TO EXTRACT ONE PDF CONTENT
def extract_pdf(pdf_path, source_root, destination_root):
    # LANGUAGE DETECTION
    identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)
    proba_language={'en':0,'fr':0}
    nb_sentences={'en':0,'fr':0}
    sentences = []
    
    # HANDLE EXTRACTION EXCEPTIONS:
    try:
        # SENTENCES EXTRACTION
        with PdfMinerWrapper(pdf_path) as doc:
            print('---------{}---------'.format(pdf_path))
            for p, page in enumerate(doc):
                for tbox in page:
                    if not isinstance(tbox, LTTextBox):
                        continue
                    for obj in tbox:
                        val = uniform(0,1)
                        if(val<=0.2):
                            l = language_detect(obj.get_text(),identifier)
                            if(l[1]>0.7):
                                proba_language[l[0]]+=l[1]
                                nb_sentences[l[0]]+=1
                        sentences.append(line_cleaner(obj.get_text()))
    except TypeError as e:
        print('{} encountered an exception:\n{}'.format(pdf_path, e))
    except Exception as ex:
        print('{} encountered an exception'.format(pdf_path))

    # CHANGE AND CREATE PATHS
    if not os.path.exists(destination_root):
        os.makedirs(destination_root)
    cleant_path = pdf_path.replace(' ', '_')
    new_path = cleant_path.replace(source_root, destination_root)     
    repertoire = '/'.join(new_path.split('/')[:-1])
    name = new_path.split('/')[-1]
    name_list = name.split('.')
    name_list[-1] = name_list[-1].lower().replace("pdf", "pdf.txt")
    title = '.'.join(name_list)

    # ENGLISH TEXTS FILTERING
    content = "\n".join(sentences)
    
    # DETECT ENGLISH FILES
    if(nb_sentences['en']!=0 and sum(nb_sentences.values())!=0):
        proba_language['en']=proba_language['en']/nb_sentences['en']
        nb_sentences['en']=nb_sentences['en']/sum(nb_sentences.values())
    
    # STOCK 
    if(nb_sentences['en']>0.7):
        # STOCK ENGLISH FILES INFO
        with open('./english_stats', 'a') as english:
            english.write("\n----english text: {}/{}----\n with english/french ratio = {}\n with average recognition = {}".format(repertoire, title, nb_sentences['en'], proba_language['en']))
            english.close()
            print("{}/{}: IS AN ENGLISH TEXT".format(repertoire, title))
    else:            
        # OR STOCK TXT FILES
        directory = repertoire.split('/')
        for d in range(1, len(directory)):
            directory[d] = '/'.join([directory[d-1], directory[d]])
            if not os.path.exists(directory[d]):
                os.makedirs(directory[d])
        with open('{}/{}'.format(repertoire, title), 'w') as txt:
            txt.write(content)
            txt.close()

# EXTRACT ALL FRENCH PDFs CONTENT INTO TXT FILES IN A NEW STRUCTURE    
for rank, pdf_path in enumerate(path_generator(sys.argv[1])):                      
    extract_pdf(pdf_path, sys.argv[1], sys.argv[2])

