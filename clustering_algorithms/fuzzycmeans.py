# -*- coding: utf-8 -*-
"""
@Fuzzy C-Means

@Variables:
    X : Normalized data set Matrix
    N : Number of Data
    c : Number of Clusters
    C : Cluster Matrix
    U : Fuzzy-Partition Matrix
    D : Fuzzy-Distance Matrix
    m : Weighting exponent
    epsilon : Termination tolerance

@author: Peter Pigler
"""
c = 3
m = 2
epsilon = 0.01
dimension = 3

import numpy as np
from random import randint
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

X = np.loadtxt("iris.csv",delimiter=',', dtype=float, usecols=tuple(range(dimension)))
N = X.shape[0]

U = np.zeros((N,c))
U_new = np.zeros_like(U)    #U partition matrix in next iteration 
D = np.zeros_like(U)
C = np.zeros((c,dimension))

#Initialize Partitionmatrix randomly
for Ui in U:
    Ui[randint(0,c-1)] = 1

#Iterate
while True:
    #Calculate cluster prototypes:
    for i in range(c):
        C[i] = np.average(X, axis = 0, weights = pow(U.T[i],m))
    
    #Calculate the distances:  
    for i in range(c):
        D[:,i] = np.apply_along_axis(np.linalg.norm,1,X-C[i])
        
    #Update the partition matrix:
    for i in range(N):
        tmp = D[i]  #Create a Distance matrix from D[i] 1-D vector
        tmp = np.repeat(tmp,c)
        tmp = tmp.reshape((c,c))
        U_new[i] = 1.0/np.dot(pow(tmp,2.0/(m-1)),pow(1.0/D[i],2.0/(m-1)))

    if np.linalg.norm(U-U_new) < epsilon:
        break   #If the distance between current U and U in the previous iteration is under terminate tolerance, halt 
    U=np.copy(U_new)

#Plot 
fig = plt.figure("FuzzyCmeans - "+str(c)+" clusters")
adat = fig.add_subplot(111,projection='3d')
adat.set_xlabel("Axis X")
adat.set_ylabel("Axis Y")
adat.set_zlabel("Axis Z")
for i in range(N):
    adat.scatter(X[i][0], X[i][1], X[i][2], c = tuple(U[i]), s = 80)
for i in range(c):
    adat.scatter(C[i][0], C[i][1], C[i][2], s = 400, marker = '+')

plt.show()   
    