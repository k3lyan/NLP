import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import sys

with open('word_count.txt', 'r') as report_titles:
    filename = [line.strip() for line in report_titles.readlines()]

vectorizer = CountVectorizer(input='filename',lowercase = True)
data_vectorized = vectorizer.fit_transform(filename)
# GET THE AMOUNT OF WORDS BY DOC
nb_mot_par_doc= np.sum(data_vectorized, axis=1)
print(len(nb_mot_par_doc))
for i in range(len(nb_mot_par_doc)):
	print(filename[i])
	print(nb_mot_par_doc[i])
