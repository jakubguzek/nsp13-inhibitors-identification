# -*- coding: utf-8 -*-

import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import pandas as pd

X = pd.read_csv('/content/subset_assay_id_embedding.csv')
chem_col = X['CHEMBL1614220']
chem_col

_, ax = plt.subplots(figsize=(10,10))
pca = PCA(n_components=2)
x_new = pca.fit_transform(X.drop(columns=['CHEMBL1614220']))
np.random.seed(2)

x_new = pd.DataFrame(x_new, columns=['PCA1', 'PCA2'])
x_new['CHEMBL1614220'] = chem_col
print(x_new)
plt.scatter(x_new['PCA1'], x_new['PCA2'], c=np.random.rand(12), alpha=0.7)
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.show()
