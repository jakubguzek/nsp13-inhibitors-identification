# -*- coding: utf-8 -*-

import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import pandas as pd

X = pd.read_csv('ligands_ecfp4.csv')

clusters = open('dice_07.txt', "r")
clust_dict = {}
for el in clusters:
  line = el.split()
  clust_dict[line[0]]=int(line[1])
clusters.close()

X['cluster'] = None

for index, row in X.iterrows():
    id_value = row['molecule_chembl_id']
    X.at[index, 'cluster'] = clust_dict[id_value]

_, ax = plt.subplots(figsize=(10,10))
pca = PCA(n_components=2)
x_new = pca.fit_transform(X.drop(columns=['molecule_chembl_id', 'cluster']))
np.random.seed(11)

x_new = pd.DataFrame(x_new, columns=['PCA1', 'PCA2'])
x_new['molecule_chembl_id'] = X['molecule_chembl_id']
x_new['cluster']= X['cluster']
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b',
          '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#1f78b4', '#ffbb78']
cl_colors = {}
for i in range(1,13):
  cl_colors[i]=colors[i-1]
plt.scatter(x_new['PCA1'], x_new['PCA2'], c=x_new['cluster'].map(cl_colors), alpha=0.7)
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.show()