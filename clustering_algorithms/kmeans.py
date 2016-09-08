# K means
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from random import randint

#-------------
#file : sourcefile
#nIterations : number of iterations
#nClusters : number of clusters
#nPoints : number of points
#Points : matrix of points
#Clusters : matrix of clusters
#-------------


# read file
X = np.loadtxt("iris.csv",delimiter = ',', dtype=float, usecols=(0,1,2))     
N = X.shape[0]
#initalize number of n. of clusters
k = input("Number of clusters: ")
#init clusters (randomize)
_c = []
while len(_c)<k:
	r=randint(0,N-1)
	if r not in _c:
		_c.append(r)      
C = X[_c]
#iteration loop
change = True
run = 0
while change and run != 10:
    mindex = np.array(range(N))
    D=np.zeros((N,k))
    for i in range(N):
		for j in range(k):
			D[i,j]=np.linalg.norm(X[i]-C[j])
		mindex[i]=list(D[i]).index(min(D[i]))
    change = False
    for i in range(k):
        in_curr_c = np.where(mindex==i)[0]
        if len(in_curr_c) != 0:
            if C[i].all != np.average(X[in_curr_c],axis=0).all:
                C[i]=np.average(X[in_curr_c],axis=0)
        run+=1

colors = [(1,0,0),(0,1,0),(0,0,1),(0,1,1),(1,0,1),(1,1,0),(1,1,1)]
fig = plt.figure("Kmeans")
adat = fig.add_subplot(111,projection='3d')
adat.set_xlabel("x tengely")
adat.set_ylabel("y tengely")
adat.set_zlabel("z tengely")
for i in range(k):
    in_curr_c = np.where(mindex==i)[0]
    tmp_X = np.array(X[in_curr_c])
    adat.scatter(tmp_X[range(len(in_curr_c)),0],tmp_X[range(len(in_curr_c)),1],tmp_X[range(len(in_curr_c)),2],
                   c=colors[i], s=80)    
    adat.scatter(C[i][0],C[i][1],C[i][2],c=colors[i],s=400)
plt.show()

        
    


