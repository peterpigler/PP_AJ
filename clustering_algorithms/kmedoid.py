#kmedoid
import numpy as np
from random import randint
from random import random
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


  ##X - pontok halmaza; N - |x|; kindex - kozeppontok vektora; C - kozeppontok matrixa; mindex - pontok mely kozepponthoz vektor; D - tavolsagmatrix
  ##in_curr_c - azonos kozeppontu pontok vektora; avg_med - kozeppont kozepe; 

#Data normalization
X = np.loadtxt("iris.csv",delimiter=',', dtype=float, usecols=(0,1,2))
N=X.shape[0]

#Get the number of clusters
k = input("k=")
nk = 0

#Initialize starting centers
kindex = []
while nk<k:
	r=randint(0,N-1)
	if r not in kindex:
		kindex.append(r)
		nk+=1        
C = X[kindex]

#Set iteration counter, generating plotcolours
run = 0
change=True
colors = [(1,0,0),(0,1,0),(0,0,1),(0,1,1),(1,0,1),(1,1,0),(1,1,1)] 
while k > len(colors):
    colors.append((random(),random(),random()))

#Iterate
while change and run != 10:
    #Calculate each points' belongings
    mindex = np.array(range(N))
    D=np.zeros((N,k))
    for i in range(N):
		for j in range(k):
			D[i,j]=np.linalg.norm(X[i]-C[j])
		mindex[i]=list(D[i]).index(min(D[i]))
    change = False
    #Calculate new medoids
    for i in range(k):
        in_curr_c = np.where(mindex==i)[0]  #pontok az i. kozeppontban
        tmp_X = np.array(X[in_curr_c])#X azon elemei, amelyek i. kozeppontban vannak
        avg_med=np.average(tmp_X,axis=0)
        tmp_D = np.zeros((len(in_curr_c),1))
        for j in range(len(in_curr_c)):
            tmp_D[j] = np.linalg.norm(tmp_X[j]-avg_med) #Tavolsagok a kozeptol, pontokra lsd. fent
        min_idx = in_curr_c[tmp_D.tolist().index(min(tmp_D.tolist()))]
        #If new center found, update
        if C[i].all != X[min_idx].all:
            change = True
            C[i] = X[min_idx]
            kindex[i] = min_idx
    run+=1

#plot, show results
fig = plt.figure("Kmedoid - "+str(k)+" clusters")
adat = fig.add_subplot(111,projection='3d')
adat.set_xlabel("Axis X")
adat.set_ylabel("Axis Y")
adat.set_zlabel("Axis Z")
for i in range(k):
    in_curr_c = np.where(mindex==i)[0]
    tmp_X = np.array(X[in_curr_c])
    adat.scatter(tmp_X[range(len(in_curr_c)),0],tmp_X[range(len(in_curr_c)),1],tmp_X[range(len(in_curr_c)),2],
                   c=colors[i], s=80)    
    adat.scatter(C[i][0],C[i][1],C[i][2],c=colors[i],s=400)
plt.show()