import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import sys
# Though the following import is not directly being used, it is required
# for 3D projection to work
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from sklearn.preprocessing import scale
from sklearn import metrics
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA
import time

# DATA PREPROCESSING 
# Define main parameters
date = time.strftime("%Y%m%d-%H:%M:%S")
n_reports = sys.argv[1]
n_clusters = sys.argv[2]
algo_name = 'clustering-visu'
algo_specificity = '{}clusters-{}reports'.format(n_clusters, n_reports)
client_name = 'thales'
livrable_name = 'livrable1'
excel_title = '{}-{}-{}-{}-{}'.format(date, algo_name, algo_specificity, client_name, livrable_name)
parameters = np.array([date, n_reports, n_clusters])
df_params = pd.DataFrame(parameters, index=['Date', 'Number of reports', 'Number of clusters'], columns = ['Parameters'])

params = {}
for i in range(len(parameters)):
    params[df_params.index[i]] = df_params.iloc[i,0]

# Prepare the OUTPUT excel file
writer = pd.ExcelWriter('{}.xlsx'.format(excel_title))

# Export the first file
df_params.to_excel(writer,'Parameters')

# Import vectors scores
df_pre = pd.read_csv('scores.csv')

#Clean Titles
df_pre.rename(columns={"Unnamed: 0": "Titles"}, inplace=True)
def rename_titles(df):
    report_names = []
    for i in range(len(df['Titles'])):
        df.loc[i, 'Titles'] = df['Titles'][i].replace(".txt", "")
rename_titles(df_pre)

# Export report names
df_index_rapports = df_pre['Titles']
df_index_rapports.to_excel(writer, 'Report Names')

# Export skill names
skills_list = list(df_pre.columns)
skills_list.remove('Titles')

def skills_cleaning(names_list):
    ids = []
    names = []
    skills = []
    for i in range(len(names_list)):
        # Titles cleaning
        names.append(names_list[i].replace(".txt", ""))
        names[i] = names[i].replace(".pkl", "")
        names[i] = names[i].replace(".json", "")
        names[i] = names[i].replace("_", " ")
        ids.append(names[i][0:4])
        names[i] = names[i][4:]
    skills.append(ids)
    skills.append(names)
    return skills

skills = skills_cleaning(skills_list)
df_skills = pd.DataFrame(skills[1], index = skills[0], columns = ['Skills'])

df_skills.to_excel(writer, 'Skill Names')

# Export vectors
df_vectors = df_pre.drop('Titles', axis=1)
def mapper_skills(skills_liste, skills):
    mapper = {}
    for i in range(len(skills_liste)):
        mapper[skills_liste[i]] = skills[0][i]
    return mapper

df_vectors.rename(columns = mapper_skills(skills_list, skills), inplace=True)
df_vectors.fillna(0.0, inplace=True)

df_vectors.to_csv('vectors.csv', index=False, sep=',')

# CLUSTERING
# Load the data from csv, put it as a dataframe
df_similarity_scores = pd.read_csv('vectors.csv')
# Normalize the data
X = normalize(df_similarity_scores, norm='l2')
# Get the normalized dataframe
df_clustering = pd.DataFramle(X, index=df_similarity_scores.index, columns=df_similarity_scores.columns)

# K-means clustering
#Fit K-Means model to the reports vectors
km = KMeans(n_clusters=n_clusters).fit(X)
#Transform the vectors coordinates into n clusters
kmeans = km.transform(X)

# CENTROIDS
#Get the centroids coordinates in the original space (47 dimensions)
centroids = km.cluster_centers_
df_centroids = pd.DataFrame(centroids, index=np.arange(n_clusters), columns=df_clustering.columns)

#Transform the centroids coordinate using kmeans
# = Distance for each centroids regarding to other centroids
data_centroids = km.transform(centroids)

# Labels
#Get the label cluster for each report vectors
labels_vectors = km.labels_
labels_centroids = np.arange(n_clusters)

df_clustering['clusters id'] = labels[0]
cols = df_clustering.columns.tolist()
cols = cols[-1:] + cols[:-1]
df_clustering = df_clustering[cols]

# Export data
# Export the whole dataFrame
df_clustering.to_csv('data_clustering.csv',index=False, sep=',')
df_clustering.to_excel(writer, 'Data Clustering', index=True)
# Export centroids skills
df_centroids.to_excel(writer, 'Centroids skill scores', index=True)
#Export median values by cluster
df_clustering.groupby('clusters id').mean().transpose().to_excel(writer, 'Clusters Means', index=True)
# Export reports cluster
df_count = df_clustering.sort_values('clusters id').groupby('clusters id').count()
df_repartition = df_count.drop(df_count.columns[1:], axis=1)
df_repartition.rename(columns={df_repartition.columns[0]: 'Reports count'}, inplace=True)
# Export number of reports by cluster
df_repartition.to_excel(writer, 'Reports Count', index=True)

# Export percentage of reports by cluster
def percentage(df, nb_reports):
    return df*100/nb_reports
df_percentage = percentage(df_repartition, n_reports)
df_percentage.rename(columns={df_percentage.columns[0]: 'Reports percentage'}, inplace=True)
df_percentage.to_excel(writer, 'Reports Percentage', index=True)

#Rajouter titres indexes
df_total = df_clustering.sort_values('clusters id')
cluster_indexes = list(df_total['clusters id'])
report_indexes = list(df_total['clusters id'].index)
hier_index = list(zip(cluster_indexes, report_indexes))
hier_index = pd.MultiIndex.from_tuples(hier_index)
df_total.set_index(hier_index, inplace=True)
df_total.drop('clusters id', axis=1, inplace =True)

df_total.to_excel(writer, 'Total Map', index=True)
writer.save()

# PCA
def data_pca(kmeans, data_centroids, dim):
    pca = PCA(n_components=dim)
    fit_pca = pca.fit(kmeans)
    vectors_pca = fit_pca.transform(kmeans)
    centroids_pca = fit_pca.transform(data_centroids)
    data_visu = np.append(vectors_pca, centroids_pca, axis = 0)
    print(data_visu.shape)
    print('RATIO VARIANCE PCA {}D: {}'.format(dim, pca.explained_variance_ratio_))
    return data_visu

# 2D
data_pca_2d = data_pca(kmeans, data_centroids, 2)
# 3D
data_pca_3d = data_pca(kmeans, data_centroids, 3)

data = pd.DataFrame(data_pca_3d, index= np.arange(n_reports+n_clusters), columns = ['x', 'y', 'z'])
cid = np.append(labels[0], labels[1], axis = 0)
data['cid'] = cid
col = data.columns.tolist()
col = col[-1:] + col[:-1]
data = data[col]
data.to_csv('data.csv',index=False, sep=',')

def visu(data_pca, dim_pca, labels, parameters):
    nb_centroids = int(parameters['Number of clusters'])
    nb_reports = int(parameters['Number of reports'])
    labels_vec = labels[0]
    labels_centro = labels[1]
    font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 16,
        }
    fignum = 1
    title = 'Data Visualization {} dimensions: {} clusters  - {} reports'.format(dim_pca, nb_centroids, nb_reports)
    fig = plt.figure(fignum, figsize=(25, 18))

    if dim_pca == 2:
        ax = fig.add_subplot(111)
        ax.scatter(data_pca[0:nb_reports, 0], data_pca[0:nb_reports, 1], c=labels_vec.astype(np.float), edgecolor='k')
        ax.scatter(data_pca[nb_reports:(nb_reports+nb_centroids), 0], data_pca[nb_reports:(nb_reports+nb_centroids), 1], c=labels_centro.astype(np.float), edgecolor='k', marker='^', s=150)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title(title, fontsize=20)
        #plt.text(10, .5, 'Date: {}'.format(parameters['Date']), 'Number of clusters: {}'.format(parameters['Number of clusters']), 'Number of reports: {}'.format(parameters['Number of reports']))
        plt.text(0.7, -0.6, parameters['Date'], fontdict=font)
        ax.dist = 30
        plt.grid(True)
        plt.savefig('{}means_pca2d'.format(nb_centroids))

    elif dim_pca == 3 :
        ax = fig.add_subplot(111, projection='3d')

        ax.scatter(data_pca[0:nb_reports, 0], data_pca[0:nb_reports, 1], data_pca[0:nb_reports, 2], c=labels_vec.astype(np.float), edgecolor='k')

        ax.scatter(data_pca[nb_reports:(nb_reports+nb_centroids), 0], data_pca[nb_reports:(nb_reports+nb_centroids), 1], data_pca[nb_reports:(nb_reports+nb_centroids), 2],                    c=labels_centro.astype(np.float), edgecolor='k', marker='^', s=150)

        ax.w_xaxis.set_ticklabels([])
        ax.w_yaxis.set_ticklabels([])
        ax.w_zaxis.set_ticklabels([])
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.set_title(title, fontsize=20)
        ax.dist = 12
        plt.grid(True)
        plt.savefig('{}means_pca3d'.format(nb_centroids))

    plt.close()

#2D
visu(data_pca_2d, 2, labels, params)
#3D
visu(data_pca_3d, 3, labels, params)
