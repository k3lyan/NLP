# -*- coding:utf-8 -*-
import numpy as np
import pandas as pd
import sys
import pyfasttext
import re
from pyfasttext import FastText
from sklearn.metrics.pairwise import cosine_similarity

#sys.argv[1]: path to the directory containing the 

# MODEL USED FOR WORD EMBEDDINGS
model = FastText()
model.load_model('./cc.fr.300.bin')

# Get the stop_words from the external file
with open('./stop_words', 'r') as sw_file:
    stop_words = [line.strip() for line in sw_file.readlines()]
    sw_file.close()

# Function to delete punctuation and useless words
def text_cleaner(text, stop_words_list):
    text = re.sub(r"[=.:><';/)(!?@\'\`\"\_\n]", r"", text)
    return [text.replace(word, '') for word in stop_words_list]


def get_doc_list(path):
    with open(path, 'r') as dl:
        list_of_doc = [line.strip() for line in dl.readlines()]
    dl.close()
    return list_of_doc

# GET REPORTS NAMES
article_names = get_doc_list('./raw_articles_titles')

def get_doc_embeddings(pathes_to_data, repertory):
    doc_vectors = []
    for absolute_path in pathes_to_data:
        with open(absolute_path, 'r') as doc:
            sentences = [text_cleaner(line.strip(), stop_words) for line in doc.readlines()]
            doc_vectors.append(np.mean([model.get_numpy_sentence_vector(sentence) for sentence in sentences], axis = 0))
            doc.close()
    return np.array(doc_vectors)

articles_embeddings = get_doc_embeddings(article_names, 'articles')

# GET SKILLS EMBEDDINGS
skills_names = get_doc_list('./raw_ipma_titles')
skills_embeddings = get_doc_embeddings(skills_names, 'skills')

# GET SCORES
def get_scores(articles_embed, skills_embed):
    return cosine_similarity(articles_embed, skills_embed)

df_scores = pd.DataFrame(get_scores(articles_embeddings, skills_embeddings), index = article_names, columns = skills_names)
df_scores.to_csv('scores.csv', index = True)
