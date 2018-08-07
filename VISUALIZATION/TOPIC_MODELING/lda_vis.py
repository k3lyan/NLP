import numpy as np
import pandas as pd
from time import time

# Sklearn
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import CountVectorizer

# Plotting tools
from termite_viz import draw_termite_plot
import pyLDAvis
import pyLDAvis.sklearn
import matplotlib.pyplot as plt

# CORPUS
report_titles = open('outputs_reports.txt', 'r')
filename = report_titles.readlines()
for i in range(len(filename)):
    filename[i] = filename[i].replace('\n', "")
    report_titles.close()

# TF
sw_english = ['docProps', 'thumbnails', 'jpeg']
max_df = 0.85
min_df = 5
tf_vectorizer = CountVectorizer(input = 'filename', max_df = max_df, min_df=min_df,\
                                        stop_words = 'english', lowercase = True ) 
def tf_model(algo, filename):
    return algo.fit(filename)

def tf_matrix(tf_vector, filename):
    return tf_vector.transform(filename)

tf_mod = tf_model(tf_vectorizer, filename)
tf_mat = tf_matrix(tf_mod, filename)
voc = tf_vectorizer.vocabulary_ 

singulars = ['avion', 'satellite', 'radar', 'opération']
plurals = ['avions', 'satellites', 'radars', 'opérations']

def delete_plurals_list(singular, plural, voc, matrix):
    for i in range(len(singular)):
        np.add(matrix[:,voc[singular[i]]], matrix[:,voc[plural[i]]]) 
        matrix[:,voc[plural[i]]] = 0
                                    
def delete_plurals(singular, plural, voc, matrix):
    matrix[:,voc[singular]] = np.add(matrix[:,voc[singular]], matrix[:,voc[plural]]) 
    matrix[:,voc[plural]] = 0

delete_plurals('risk', 'risks', voc, tf_mat)
delete_plurals('opportunity', 'opportunities', voc, tf_mat)
delete_plurals('project', 'projects', voc, tf_mat)
delete_plurals('resource', 'resources', voc, tf_mat)
delete_plurals('conflict', 'conflicts', voc, tf_mat)

# LDA
n_reports = tf_mat.shape[0]
n_words = tf_mat.shape[1]
n_topics = 7
n_top_words = 30

# Materialize the sparse data
tf_dense = tf_mat.todense()
# Compute Sparsicity = Percentage of Non-Zero cells
print("Sparsicity: ", ((tf_dense > 0).sum()/tf_dense.size)*100, "%")
print("Fitting LDA models with %d topics, ""%d docs, %d words..." % (n_topics, n_reports, n_words))

lda = LatentDirichletAllocation(n_components=n_topics, max_iter=10,\
                                learning_method='batch',\
                                learning_offset=50.,\
                                learning_decay=0.9,\
                                random_state=0)

t0 = time()
model = lda.fit(tf_mat)

print("done in %0.3fs." % (time() - t0))
# Log Likelyhood: Higher the better
print("Log Likelihood: ", lda.score(tf_mat))
# Perplexity: Lower the better. Perplexity = exp(-1. * log-likelihood per word)
print("Perplexity: ", lda.perplexity(tf_mat))
tf_feature_names = tf_vectorizer.get_feature_names()

# DRAW TERMITE OF TOP WORDS
def top_words(model, feature_names, n_top_words):
    terms_tmp = []
    for topic_idx, topic in enumerate(model.components_):
        terms_tmp.append([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]])
    terms_list = []
    for i in range(len(terms_tmp)):
        terms_list += terms_tmp[i]
        terms = set(terms_list)
    return terms

terms = top_words(model, tf_feature_names, n_top_words)
print('Number of terms: {}'.format(len(terms)))

def top_tf(model, top_terms, voc): 
    # For each main terms
    ids = []
    top = []
    for w, word in enumerate(top_terms):
        # for each topics
        ids.append(voc[word])
        top.append([])
        for i in range(n_topics):
            top[w].append(model.components_[i][ids[w]])
    return top

#voc: tf_vectorizer.vocabulary_ --> dico: keys = terms, values = ids
#feature_names: tf_vectorizer.get_feature_names() --> list: feature names depending on the index
                                                                                                                            
top = top_tf(model, terms, voc)
topics = ['Topic {}'.format(i) for i in range(n_topics)]
termite_fig = draw_termite_plot(np.array(top), topics, terms)
termite_fig.plot()
plt.savefig('tm.png', bbox_inches='tight')

# DRAW pyLDAvis
pyLDAvis.enable_notebook()
panel = pyLDAvis.sklearn.prepare(lda, tf_mat, tf_vectorizer, mds='tsne', R=10, sort_topics = False)
pyLDAvis.save_html(panel, "tm.html")



