# K means

"""
@Kmeans

@author: Peter Pigler
"""
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from random import randint
import Param

c = Param.c
m = Param.m
e = Param.e

import Data

X = Data.X
[N,n] = map(int, X.shape)
f = np.zeros_like(X.T[0])

f_new = np.zeros_like(f)    #f partition matrix in next iteration
d=np.zeros((N,c))
v = np.zeros((c,n))

#Initialize Cluster matrix randomly
for i in range(c):
    v[i] = X[randint(0,N-1)]
    while not v[np.where(v == v[i])].all():
        print v[i]
        v[i] = X[randint(0,N-1)]

#Iterate
run = 0
while True and run != 20:
    for i in range(c):
        d[:,i] = np.apply_along_axis(np.linalg.norm,1,X-v[i])
    f_new = np.argmin(d, axis = 1)
    for i in range(c):
        if np.size(d[np.where(f_new == i)]):
            v[i] = np.mean(X[np.where(f_new == i)], axis = 0)
        else:
            v[i] = np.zeros_like(v[i])
    if np.linalg.norm(f-f_new) < e:
        break   #If the distance between current partition vector (f_new) and previously iterated p. vector (f) is under terminate tolerance, halt
    f=np.copy(f_new)
    run+=1

colors = [(1,0,0),(0,1,0),(0,0,1),(0,1,1),(1,0,1),(1,1,0),(1,1,1)]
fig = plt.figure("Kmeans - "+str(c)+" clusters")
adat = fig.add_subplot(111,projection='3d')
adat.set_xlabel("x tengely")
adat.set_ylabel("y tengely")
adat.set_zlabel("z tengely")
for i in range(N):
    adat.scatter(X[i][0], X[i][1], X[i][2], c = colors[f[i]])
for i in range(c):
    adat.scatter(v[i][0],v[i][1],v[i][2],c=colors[i],s=400)
plt.show()





