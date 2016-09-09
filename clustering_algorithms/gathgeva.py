# -*- coding: utf-8 -*-
"""
@Gath Geva

@Variables:
    X : Normalized data set Matrix
    N : Number of Data
    c : Number of Clusters
    C : Cluster Matrix
    U : Fuzzy-Partition Matrix
    D : Fuzzy-Distance Matrix
    F : Fuzzy-Covariance Matrix w/ U[im]^2 weights
    m : Weighting exponent
    epsilon : Termination tolerance

@author: Peter Pigler
"""
c = 3;
m = 2;
epsilon = 0.01


import numpy as np
from random import randint
from math import pi, sqrt, exp
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


#Data normalization
X = np.loadtxt("iris.csv",delimiter = ',', dtype = float, usecols=(0,1,2))
[N, n] = map(int, X.shape)
U = np.zeros((N,c))
U_new = np.zeros_like(U)    #U partition matrix in next iteration 
D = np.zeros_like(U)
C = np.zeros((c,n))

#Initialize Partitionmatrix randomly
for i in range(N):
    U[i][randint(0,c-1)] = 1

run = 0

F = np.zeros((c,n,n))   #covariance matrix

while True and (run != 1):
    #Calculate cluster prototypes:
    for i in range(c):
        C[i] = np.average(X, axis = 0, weights = pow(U.T[i],m))

    #Calculate prior probability
    a = 1.0/N*pow(U,m).sum(axis = 0)   #gives prior probability of selecting i-th cluster 
        
    #Calculate F covariance matrix, weighted by U
    for i in range(c):        
        np.fill_diagonal(F[i],1)            
        Xk = X-C[i]
        Xk = np.multiply(Xk,pow(U.T[i],m)[:, np.newaxis])
        F[i] = np.cov(Xk.T)
        
        A = np.dot(pow(np.linalg.det(F[i]),1.0/n),np.linalg.pinv(F[i]))
        #for j in range(N):
        #    D[j,i] = sqrt(np.dot((np.dot((X[j]-C[i]),A)),X[j]-C[i])) 
        #Calculate the distances:    
        #AA = 1/pow(np.linalg.det(np.linalg.pinv(F[i])),n/2.)*1/a[i]  #meg kell nézni
        B = np.exp(1./2*sqrt(np.dot((np.dot(X-C[i],A),np.linalg.pinv(F[i]))),X-C[i]))
        D[i] = A*B
        #for j in range(N):        
            #D[j,i] = A*np.exp(1/2.*np.sum(np.dot(np.dot((X-C[i]),np.linalg.pinv(F[i])) , (X-C[i]).T)))
    #Update the partition matrix:
    for i in range(N):
        tmp = D[i]  #Create a Distance matrix from D[i] 1-D vector
        tmp = np.repeat(tmp,c)
        tmp = tmp.reshape((c,c))
        U_new[i] = 1.0/np.dot(pow(tmp,2.0/(m-1)),pow(1.0/D[i],2.0/(m-1)))    

        
    if np.linalg.norm(U-U_new) < epsilon:
        break   #If the distance between current U and U in the previous iteration is under terminate tolerance, halt
    U = np.copy(U_new)
    run += 1    

#Plot
fig = plt.figure("GathGeva Clustering - "+str(c)+" clusters")
adat = fig.add_subplot(111,projection='3d')
adat.set_xlabel("Axis X")
adat.set_ylabel("Axis Y")
adat.set_zlabel("Axis Z")
for i in range(N):
    adat.scatter(X[i][0], X[i][1], X[i][2], c = tuple(U[i]), s = 80)
for i in range(c):
    adat.scatter(C[i][0], C[i][1], C[i][2], s = 400, marker = '+')

plt.show()   
