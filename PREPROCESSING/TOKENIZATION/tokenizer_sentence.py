import spacy
import sys
import numpy as np
import textacy
import os

#nlp = spacy.load('/absolute_path_to/fr_core_news_sm-2.0.0/fr_core_news_sm/fr_core_news_sm-2.0.0')
nlp = spacy.load('fr')

def path_generator(initial_root):
    """Get the relative paths of all files in the (sub)directories contained in the initial_root directory and return it as a list."""
    for root, dirs, files in os.walk(initial_root):
        paths = [os.path.join(root, name) for name in files]
    return paths

def txt_to_sentences(file_title):
    """Tokenize a txt file given into sentences where each token is seperated by a whitespace and return a list of these sentences."""
    with open(file_title, "r") as text:
        # Preprocessing from text
        text = str(text.read())
        text=textacy.preprocess.normalize_whitespace(text)
        text=textacy.preprocess.fix_bad_unicode(text, normalization=u'NFKC')
        text=textacy.preprocess.unpack_contractions(text)
        # Sentence and word separation with SPACY
        nlp_text=nlp(text)
        sentences_Spacy = list(nlp_text.sents)
        sents = [" ".join([w.text for w in sent]) for sent in nlp_text.sents]
        return sents 

def tokenize_files(paths, source_root, destination_root):
    """Tokenize all the files in a new arborescence."""
    for p, path in enumerate(paths):
        # CHANGE AND CREATE PATHS
        if not os.path.exists(destination_root):
            os.makedirs(destination_root)
        new_path = path.replace(source_root, destination_root)     
        repertoire = '/'.join(new_path.split('/')[:-1])
        title = new_path.split('/')[-1]
        # CREATE THE NEW ARBORESCENCE
        directory = repertoire.split('/')
        for d in range(1, len(directory)):
            directory[d] = '/'.join([directory[d-1], directory[d]])
            if not os.path.exists(directory[d]):
                os.makedirs(directory[d])
        # WRITE TOKENIZED FILES
        with open('{}/{}'.format(repertoire, title), 'w') as tokenized_txt:

            tokenized_txt.write("\n".join(txt_to_sentences(path)))
            tokenized_txt.close()
        print('{}/{}'.format(repertoire, title))

tokenize_files(path_generator(sys.argv[1]), sys.argv[1], sys.argv[2])
