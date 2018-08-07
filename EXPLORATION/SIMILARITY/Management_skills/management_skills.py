import numpy as np
import pandas as pd
import sys
import os
import pyfasttext
import re
from pyfasttext import FastText
from sklearn.metrics.pairwise import cosine_similarity

# MODEL USED FOR WORD EMBEDDINGS
model = FastText()
model.load_model('path_to_fasttext_embeddings/cc.fr.300.bin')

# Get the stop_words from the external file
with open('./stop_words', 'r') as sw_file:
    stop_words = [line.strip() for line in sw_file.readlines()]
    sw_file.close()

def text_cleaner(text, stop_words_list):
     '''Delete punctuation and words from the stop worrds list.'''
    text = re.sub(r"[=.:><';/)(!?@\'\`\"\_\n]", r"", text)
    return [text.replace(word, '') for word in stop_words_list]

def path_generator(initial_root):
    '''Generate the list of file paths located in the arborescence starting at the initial_root.'''
    for root, dirs, files in os.walk(initial_root):
        paths = [os.path.join(root, name) for name in files]
    return paths

# GET REPORTS NAMES
article_names = path_generator('../../../PREPROCESSING/DATA_STATS/Articles')

def get_doc_embeddings(pathes_to_data):
    doc_vectors = []
    for path in pathes_to_data:
        with open(path, 'r') as doc:
            sentences = [text_cleaner(line.strip(), stop_words) for line in doc.readlines()]
            doc_vectors.append(np.mean([model.get_numpy_sentence_vector(sentence) for sentence in sentences], axis = 0))
            doc.close()
    return np.array(doc_vectors)

articles_embeddings = get_doc_embeddings(article_names)

# GET SKILLS EMBEDDINGS
skills_names = path_generator('../../../PREPROCESSING/DATA_STATS/IPMA')
skills_embeddings = get_doc_embeddings(skills_names)

# GET SCORES
def get_scores(articles_embed, skills_embed):
    return cosine_similarity(articles_embed, skills_embed)

df_scores = pd.DataFrame(get_scores(articles_embeddings, skills_embeddings), index = article_names, columns = skills_names)
df_scores.to_csv('scores.csv', index = True)
