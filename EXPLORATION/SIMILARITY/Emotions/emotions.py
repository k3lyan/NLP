import numpy as np
import os
import sys
import pyfasttext
from pyfasttext import FastText
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

#sys.argv[1]: the targeted root directory where is located the text files ready to be emotionally evaluated
#sys.argv[2]: the threshold for the cosine similarity calculation

# MODEL USED FOR WORD EMBEDDINGS
model = FastText()
model.load_model('path_to_the_fasttext_embedding_model/cc.fr.300.bin')

def path_generator(initial_root):
    '''Generate the list of file paths located in the arborescence starting at the initial_root.'''
    for root, dirs, files in os.walk(initial_root):
        paths = [os.path.join(root, name) for name in files]
    return paths

def get_emotions_lists(initial_root)
    '''Get a list of synonyms of emotions from the files contained in initial root directory and returns a list of it.'''
    emotions_lists = path_generator(initial_root)
    emotion = []
    names = []
    for p, path in enumerate(emotions_lists):
        with open(path, 'r') as emotion_file:
            emotion.append([synonym.strip() for synonym in emotion_file.readlines()])
            names.append(path.split('/')[-1])
            emotion_file.close()
    return (emotion, names)

emotion = get_emotions_lists('./emotions_list')[0]

def emotion_mat(emotion_words_list):
    mat = []
    for vec in emotion_words_list:
        mat.append(np.mean([model.get_numpy_vector(word) for word in vec], axis=0))
    return np.array(mat)

emotions_matrix = emotion_mat(emotion)

# GET TXT FILES PATHS
filename = path_generator(sys.argv[1])

# COUNT VECTORIZED THE TXT FILES
vectorizer = CountVectorizer(input='filename', lowercase = True)
data_vectorized = vectorizer.fit_transform(filename)
vocab = sorted(vectorizer.vocabulary_, key=vectorizer.vocabulary_.get)

# GET THE AMOUNT OF WORDS BY DOC
nb_mot_par_doc= np.sum(data_vectorized, axis=1)
print('NUMBER OF WORDS PER DOC: \n{}\n'.format(len(nb_mot_par_doc)))

# GET THE EMBEDDINGS FOR EACH WORD OF THE VOCABULARY
word_vectors = np.array([model.get_numpy_vector(word) for word in vocab])

seuil = float(sys.argv[2])
def get_similarity_matrix(mean_embedding_emotion,word_vectors,seuil):
    return(cosine_similarity(mean_embedding_emotion,word_vectors)>seuil)

binary_similarity_matrix = get_similarity_matrix(emotions_matrix, word_vectors, seuil)

#retourne une liste de matrice_emotion. L'élément i de la liste correspond à une matrice pour chaque émotion.
#La matrice a pour format nb_doc * nb_total mot
#prend en entrée la matrice de 0-1 et une matrice nb_doc * nb_mots issue du comptage

def matrix_by_emotion(binary_similarity_matrix, data_vectorized):
    list_matrix_emotion = []
    for i in range(len(binary_similarity_matrix)):
        emotion= data_vectorized.toarray()*np.array(binary_similarity_matrix[i,:])
        list_matrix_emotion.append(emotion)
    return(list_matrix_emotion)

list_matrix_emotion = matrix_by_emotion(binary_similarity_matrix, data_vectorized)

def create_df_suppr_0_column(matrice_1_emotion,rapport_title, vocab):
    df=pd.DataFrame(matrice_1_emotion,columns=vocab)
    df[df==0] = np.nan
    df=df.dropna(axis=1,how='all')
    df.fillna(0)
    return (df)

nom_emotion =  get_emotions_lists('./emotions_list')[1]

# RESULTS FOR DIFFERENT THRESHOLD VALUES
for i in range(len(list_matrix_emotion)):
    df= create_df_suppr_0_column(list_matrix_emotion[i],rapport_title,vocab)
    file_output= 'test{}'.format(nom_emotion[i])
    directory = './{}/'.format(str(seuil))
    if not os.path.exists(directory):
        os.makedirs(directory)
    df.to_csv('{}{}.csv'.format(directory, file_output), index=True)

def matrix_emotion_doc(list_matrix_emotion, rapport_title, nom_emotion, nb_mot_par_doc):
    matrix_emotion_par_doc=np.zeros((len(rapport_title),len(nom_emotion)+1))
    for doc in range(len(list_matrix_emotion[0])):
        for emotion in range(len(list_matrix_emotion)):
            matrix_emotion_par_doc[doc,emotion]=sum(list_matrix_emotion[emotion][doc,:])/nb_mot_par_doc[doc]
            matrix_emotion_par_doc[doc,len(nom_emotion)]=sum(matrix_emotion_par_doc[doc,:])
        df=pd.DataFrame(matrix_emotion_par_doc,index=rapport_title,columns=nom_emotion+['Total'])
        file_output='Percentage_per_emotion_per_doc'
        directory = './{}/'.format(str(seuil))
        if not os.path.exists(directory):
            os.makedirs(directory)
        df.to_csv('{}{}.csv'.format(directory, file_output), index=True)

matrix_emotion_doc(list_matrix_emotion, filename, nom_emotion, nb_mot_par_doc)

