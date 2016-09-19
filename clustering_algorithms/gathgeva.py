# -*- coding: utf-8 -*-
"""
@GGClust

@author: Peter Pigler
"""
import numpy as np
from random import randint
from math import pi, sqrt, exp
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import Param

c = Param.c
m = Param.m
e = Param.e

import Data

X = Data.X
[N, n] = map(int, X.shape)
f = np.zeros((N,c))
f_new = np.zeros_like(f)    # f partition matrix in next iteration
d = np.zeros_like(f)
v = np.zeros((c,n))

# Initialize Partition matrix randomly
for i in range(N):
    f[i][randint(0,c-1)] = 1

# Initialize Cluster matrix randomly
for i in range(c):
    v[i] = X[randint(0,N-1)]
    while not v[np.where(v == v[i])].all():
        v[i] = X[randint(0,N-1)]

for i in range(c):
    d[:, i] = np.apply_along_axis(np.linalg.norm, 1, X - v[i])

run = 0

P = np.zeros((c,n,n))   # covariance matrix

while True and (run != 2):

    # Update the partition matrix:
    for i in range(N):
        tmp = d[i]
        tmp = np.repeat(tmp,c)
        tmp = tmp.reshape((c,c))
        f[i] = 1.0/np.dot(pow(tmp,2.0/(m-1)),pow(1.0/d[i],2.0/(m-1)))
    f[np.isnan(f)] = 1
    # Calculate cluster prototypes:
    fm = pow(f,m)
    for i in range(c):
        v[i] = np.average(X, axis = 0, weights = fm.T[i])

    # Calculate prior probability
    Pi = 1.0/N*fm.sum(axis = 0)   # gives prior probability of selecting i-th cluster

    # Calculate F covariance matrix, weighted by U
    for i in range(c):
        # np.fill_diagonal(P[i],1)
        Xf = X-v[i]
        Xf = np.multiply(Xf,fm.T[i][:, np.newaxis])
        P[i] = np.cov(Xf.T)
        #A = np.dot(pow(np.linalg.det(P[i]), 1.0 / n), np.linalg.inv(P[i]))
        AA = 1/pow(np.linalg.det(np.linalg.pinv(P[i])),n/2.)*1/Pi[i]  #meg kell nézni
        A = np.dot(pow(np.linalg.det(P[i]), 1.0 / n), np.linalg.inv(P[i]))
        for j in range(N):
            #d[j, i] = AA*np.exp(1./2.*np.dot((np.dot((X[j] - v[i]), np.linalg.inv(P[i]))), X[j] - v[i]))
            d[j, i] = AA * exp(1. / 2. * np.dot((np.dot((X[j] - v[i]),A)), X[j] - v[i]))
            # d[j,i] = sqrt(1./sqrt(np.linalg.det(np.linalg.pinv(P[i])))*1./Pi[i]*exp((1./2.)*np.dot(np.dot(X[j] - v[i], np.linalg.inv(P[i])),X[j] - v[i])))
        #B = np.exp(1./2*np.dot(pow(np.linalg.det(P[i]),1.0/n),np.linalg.pinv(P[i])))
        # Calculate the distances:
        #AA = 1/pow(np.linalg.det(np.linalg.pinv(F[i])),n/2.)*1/a[i]  #meg kell nézni
        #A = sqrt(np.linalg.det(np.linalg.pinv(P[i])))/Pi[i]

        # d[:,i] =
        #for j in range(N):        
            #D[j,i] = A*np.exp(1/2.*np.sum(np.dot(np.dot((X-C[i]),np.linalg.pinv(F[i])) , (X-C[i]).T)))
    # Update the partition matrix:
    for i in range(N):
        tmp = d[i]  # Create a Distance matrix from D[i] 1-D vector
        tmp = np.repeat(tmp,c)
        tmp = tmp.reshape((c,c))
        f_new[i] = 1.0/np.dot(pow(tmp,2.0/(m-1)),pow(1.0/d[i],2.0/(m-1)))


    if np.linalg.norm(f-f_new) < e:
        break   # If the distance between current U and U in the previous iteration is under terminate tolerance, halt
    f = np.copy(f_new)
    run += 1
"""
#Plot
fig = plt.figure("GathGeva Clustering - "+str(c)+" clusters")
adat = fig.add_subplot(111,projection='3d')
adat.set_xlabel("Axis X")
adat.set_ylabel("Axis Y")
adat.set_zlabel("Axis Z")
for i in range(N):
    adat.scatter(X[i][0], X[i][1], X[i][2], c = tuple(f[i]), s = 80)
for i in range(c):
    adat.scatter(v[i][0], v[i][1], v[i][2], s = 400, marker = '+')

plt.show()
"""