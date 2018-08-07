import matplotlib
import textacy
import sys
#from nltk.stem.lancaster import LancasterStemmer
#from nltk.stem import WordNetLemmatizer

st = LancasterStemmer()
wnl = WordNetLemmatizer()

doc = []
for i in range(1,6):
    file = open('./rapport{}.txt'.format(i), 'r')
    with open('./articles{}.txt'.format(i), 'r') as article:
        doc.append(article.read())
        doc[i-1] = doc[i-1].replace('\n', "").replace('.', "").lower().split(" ")
    article.close()
                                    
vectorizer = textacy.Vectorizer(tf_type='linear', apply_idf=True, idf_type='smooth', min_df=3, max_df=0.9)
doc_term_matrix = vectorizer.fit_transform(doc)
model = textacy.tm.TopicModel('lda', n_topics=10)
model.fit(doc_term_matrix)
model.termite_plot(doc_term_matrix, vectorizer.id_to_term, topics=-1,  n_terms=20, sort_terms_by='seriation')
