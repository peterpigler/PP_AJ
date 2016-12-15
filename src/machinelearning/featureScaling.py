import theano
import theano.tensor as T
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

data = pd.read_excel('DataOverview.xlsx')
data = data.fillna(0)
labels = data['CITY_NAME'].as_matrix()
print labels

data = np.array(data.drop(['CITY_NAME', 'CITY_ID'], axis=1).as_matrix())
[N,n] = map(int,data.shape)
# Feature scaling
for i in range(n):
    #data.T[i] = (data.T[i] - np.nanmean(data.T[i],axis = 0)) / (np.nanmax(data, axis =0)[i]-np.nanmin(data,axis=0)[i])
    data.T[i] = (data.T[i] - np.nanmean(data.T[i], axis=0)) / np.std(data.T[i], axis = 0)


# v = theano.shared('v')
# X = T.matrix('X')
# Xv = T.dot(X,v)
# evals, evecs = np.linalg.eig(data)
#cost = T.dot(Xv.T, Xv) - np.sum(evals[j]*T.dot(evecs[j],v)*T.dot(evecs[j],v) for j in xrange(i))
# gv = T.grad(cost, v)

pca = PCA()
pca.fit(data)
print pca.fit(data)
print pca.explained_variance_ratio_
print pca.fit_transform(data)

#Plot
plt.scatter(pca.fit_transform(data).T[0],pca.fit_transform(data).T[1])
plt.text(pca.fit_transform(data).T[0],pca.fit_transform(data).T[1], labels.T)
plt.show()