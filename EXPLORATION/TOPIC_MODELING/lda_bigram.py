import os
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

path = "/home/output/extracted_0"
filelist = []

for root, dirs, files in os.walk(path):
    for filename in files:
        filelist.append(os.path.join(root, filename))

garbage = re.compile('[0-9\ -/:-@\[-`{-~’‐\u2000-\u200F\u00A0\u2028-\u202F\u2010-\u2027\u2030-\u203A´«»¡¿−·\ufffd\uf0a0-\uf0ff\uf020-\uf08f\u20ac\u25a0\u25ba\u0001-\u0019\u02c6\u02c7\u02da-\u02df\u0e00\u06de\u00a6-\u00a8]')

def prep(sentence):
    return garbage.sub(" ", sentence.strip().lower().replace('\ufb02', 'fi').replace('ﬁ', 'fi'))

stop_words_fr = []
with open("default_stop_words.txt", "r") as sfile:
    for l in sfile:
        stop_words_fr.append(l.lower().strip())

tf_vectorizer = CountVectorizer(input='filename',
        preprocessor=prep,
        stop_words=stop_words_fr,
        analyzer='word',
        token_pattern=r'\b[^0-9\t\r\n\ -/:-@\[-`{-~’]+\w+\b',
        max_df=0.9, min_df=5)

bigram_req = ["piste accès", "puits blindé", "mise service", "arrêt chute",
        "tête puit", "piège cailloux", "massif ancrage", "pilote opérationnel",
        "pilote stratégique", "points arrêt", "conduite forcée",
        "revêtement anticorrosion", "rupture frettes",
        "reconnaissances géologiques", "vanne tête", "qualité tôles",
        "qualité soudures", "rénovation de la CF", "accident travail"]

tf = tf_vectorizer.fit_transform(filelist)

ncomp = 13
n_top_words = 10
lda = LatentDirichletAllocation(n_components=ncomp,
        max_iter=10,
        learning_method='online',
        learning_offset=50.,
        random_state=0)
lda.fit(tf)
tf_feature_names = tf_vectorizer.get_feature_names()

for topic_idx, topic in enumerate(lda.components_):
    print("Topic :",topic_idx)
    msg = " ".join([tf_feature_names[i]
        for i in topic.argsort()[:-n_top_words - 1:-1]])
    print(msg)
    print()
