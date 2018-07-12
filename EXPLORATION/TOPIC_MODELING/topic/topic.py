from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation, NMF
import numpy as np
from scipy.sparse.linalg import svds
from gensim import corpora, models
from hlda.sampler import HierarchicalLDA
#import corex.corex_topic as ct


def do_lsa(corpus, topic_count, remove_tokens=None,
           is_lower=True, remove_accents='ascii', max_in_corpus=1.0):
    """Latent Semantic Analysis or Latent Semantic Indexing"""

    tfidf_vectorizer = TfidfVectorizer(max_df=max_in_corpus,
                                       lowercase=is_lower,
                                       stop_words=remove_tokens,
                                       strip_accents=remove_accents)

    # tf-idf features
    tfidf_info = tfidf_vectorizer.fit_transform(corpus)

    # SVD
    U, singularValues, V = svds(tfidf_info, k=topic_count)

    word_topic_matrix = np.dot(tfidf_info.todense().T, U)
    document_topic_matrix = np.dot(tfidf_info.todense(), V.T)
    return word_topic_matrix, \
        tfidf_vectorizer.get_feature_names(), document_topic_matrix


def do_lda(corpus, topic_count, remove_tokens=None,
           is_lower=True, remove_accents='ascii', max_in_corpus=0.95):
    """Latent Dirichlet Allocation using scikit-learn library"""

    count_vectorizer = CountVectorizer(max_df=max_in_corpus,
                                       strip_accents=remove_accents,
                                       stop_words=remove_tokens,
                                       lowercase=is_lower)
    tf_info = count_vectorizer.fit_transform(corpus)

    # Latent Dirichlet Allocation
    lda = LatentDirichletAllocation(n_components=topic_count,
                                    learning_method='batch',
                                    learning_offset=50.,
                                    random_state=1)
    lda.fit(tf_info)
    word_topic_matrix = lda.components_.T
    document_topic_matrix = lda.transform(tf_info)

    return word_topic_matrix, count_vectorizer.get_feature_names(), \
        document_topic_matrix


def do_nmf(corpus, topic_count, remove_tokens=None,
           is_lower=True, remove_accents='ascii', max_in_corpus=0.95):
    """Non-Negative Matrix Factorization using scikit-learn library"""

    tfidf_vectorizer = TfidfVectorizer(max_df=max_in_corpus,
                                       lowercase=is_lower,
                                       stop_words=remove_tokens,
                                       strip_accents=remove_accents)
    # tf-idf features
    tfidf_info = tfidf_vectorizer.fit_transform(corpus)

    # Non-negative matrix
    nmf = NMF(n_components=topic_count,
              random_state=1,
              alpha=.1,
              l1_ratio=.5)
    nmf.fit(tfidf_info)
    word_topic_matrix = nmf.components_.T
    document_topic_matrix = nmf.transform(tfidf_info)

    return word_topic_matrix, tfidf_vectorizer.get_feature_names(), \
        document_topic_matrix


def do_hdp(corpus):
    """Hierarchical Dirichlet Process using gensim library"""

    dictionary = corpora.Dictionary(corpus)
    gensim_corpus = [dictionary.doc2bow(text) for text in corpus]
    hdp = models.HdpModel(gensim_corpus, dictionary)

    return hdp, gensim_corpus


def do_hlda(corpus, depth=4):
    """Hierarchical LDA using joewandy's hlda library"""

    words = set([word for doc in corpus for word in doc])
    words_dic = {word: idx for idx, word in enumerate(words)}
    docs = [[words_dic[word] for word in text] for text in corpus]

    hlda = HierarchicalLDA(docs,
                           list(words),
                           alpha=10.0,  # smoothening over
                           # level distributions
                           gamma=1.,  # CRP smoothening parameter;
                           # number of imaginary customers at next,
                           # as of now empty table
                           eta=0.1,  # smoothening over
                           # topic-word distributions
                           num_levels=depth)
    hlda.estimate(500,  # iterations for the sampler
                  display_topics=502,  # print summary after iterations
                  n_words=0,  # the number of most probable words
                  with_weights=False)

    return hlda


def do_corex(corpus, topic_count, remove_tokens=None,
             is_lower=True, remove_accents='ascii', max_in_corpus=0.95):
    """Anchored CorEx: Topic Modeling with Minimal Domain Knowledge"""

    count_vectorizer = CountVectorizer(max_df=max_in_corpus,
                                       strip_accents=remove_accents,
                                       stop_words=remove_tokens,
                                       lowercase=is_lower)

    tf_info = count_vectorizer.fit_transform(corpus)

    words = list(np.asarray(count_vectorizer.get_feature_names()))

    topic_model = ct.Corex(n_hidden=topic_count, words=words, max_iter=200,
                           verbose=False, seed=None)
    topic_model.fit(tf_info, words=words)
    return topic_model
