import spacy
import sys
import numpy as np
import textacy

nlp = spacy.load('fr')

def txt_to_sentences(file_title):
    with open(file_title, "r") as text:
        # Preprocessing from text
        text = str(text.read())
        text=textacy.preprocess.normalize_whitespace(text)
        text=textacy.preprocess.fix_bad_unicode(text, normalization=u'NFKC')
        text=textacy.preprocess.unpack_contractions(text)
        # Sentence and word separation with SPACY
        nlp_text=nlp(text)
        sentences_Spacy = list(nlp_text.sents)
        # with only lowercase, it works better
        sents = [" ".join([w.text for w in sent]) for sent in nlp_text.sents]
        return sents 

# WRITE TOKENIZED TEXTS IN NEW FILES
def tokenized_files():
    with open(sys.argv[1], "r") as titles_list:
        filenames = [line.strip() for line in titles_list.readlines()]
        titles_list.close()
    if (sys.argv[1] == 'raw_articles_titles'):
        rep = 'ARTICLES'
    elif (sys.argv[1] == 'raw_ipma_titles'):
        rep = 'IPMA'
    else:
        rep = 'TEST'

    for title in filenames:
        new_title = title.replace(" ", "_")
        new_title = title.replace(".pdf", ".txt")
        new_title = new_title.split('/')[-1]
        print(new_title)
        with open('./{}/OUTPUTS/{}'.format(rep, new_title), "w") as tokenized_file:
            tokenized_file.write("%s\n" % item for item in txt_to_sentences(title))
            tokenized_file.close()

tokenized_files()
