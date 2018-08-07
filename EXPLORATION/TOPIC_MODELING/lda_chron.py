import os
import pandas as pd
from collections import defaultdict
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation

#sys.argv[1]: path of the targeted root directory

stop_words_fr = []
with open('stop_words.txt', "r") as sfile:
    for l in sfile:
        stop_words_fr.append(l.lower().strip())

path = sys.argv[1]
table = {}
for dirs in os.listdir(path):
    print(dirs)
    table[dirs] = defaultdict(list)
    filelist = []
    root = os.path.join(path, dirs)
    for f in os.listdir(root):
        filelist.append(os.path.join(root, f))
    print("files", len(filelist))
    if len(filelist) <= 1:
        continue
    tf_vectorizer = CountVectorizer(input='filename',
        stop_words = stop_words_fr,
        token_pattern=r'\b[^0-9\t\r\n\ -/:-@\[-`{-~’]+\w+\b',
        max_df=0.9, min_df=5)

    tf = tf_vectorizer.fit_transform(filelist)

    ncomp = 5
    n_top_words = 5
    lda = LatentDirichletAllocation(n_components=ncomp,
        max_iter=7,
        learning_method='online',
        learning_offset=50.,
        random_state=0)
    print("lda")
    lda.fit(tf)
    tf_feature_names = tf_vectorizer.get_feature_names()

    for topic_idx, topic in enumerate(lda.components_):
        for i in topic.argsort():
            score = topic[i]/topic.sum()
            table[dirs][tf_feature_names[i]].append(score)
df_list = []
for year in sorted(table.keys()):
    for word in table[year]:
        df_list.append([year, word, sum(table[year][word])])

df = pd.DataFrame(df_list)
df.to_csv("lda_timeline.csv")
