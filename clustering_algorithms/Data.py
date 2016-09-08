import numpy as np

X = np.loadtxt("iris.csv", usecols=(0,1,2), delimiter=',')
Xold = np.copy(X)
min = np.min(X, axis = 0)
max = np.max(X, axis = 0)
mean = np.max(X, axis = 0)
std = np.std(X, axis = 0)
