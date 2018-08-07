from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import Normalizer
from sklearn.cluster import KMeans
import numpy as np


def do_kmeans(corpus, num_clusters, top_words=10, remove_tokens=None,
              is_lower=True, remove_accents='ascii', max_in_corpus=1.0):
    """K-Means clustering using scikit-learn library"""

    tfidf_vectorizer = TfidfVectorizer(max_df=max_in_corpus,
                                       lowercase=is_lower,
                                       stop_words=remove_tokens,
                                       strip_accents=remove_accents)
    tfidf_info = tfidf_vectorizer.fit_transform(corpus)
    normalizer = Normalizer(copy=False)
    norm_X = normalizer.fit_transform(tfidf_info)

    km_model = KMeans(n_clusters=num_clusters, init='k-means++',
                      max_iter=300, n_init=10)
    km_model.fit(norm_X)
    cluster_words = np.argsort(km_model.cluster_centers_)
    words = tfidf_vectorizer.get_feature_names()
    cluster_top_words = []
    for cluster in cluster_words:
        cluster_top_words.append([words[i] for i in cluster[-top_words:]])

    return km_model.labels_, cluster_top_words
