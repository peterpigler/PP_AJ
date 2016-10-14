# -*- coding: utf-8 -*-
"""
@KMedoid

@author: Peter Pigler
"""
import numpy as np
from random import randint
from random import random
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


def kmedoid(Data, Param):


    if  Param.has_key('c'):  c = Param['c']
    else:   c = 6
    if Param.has_key('m'):   m = Param['m']
    else:   m = 2
    if Param.has_key('e'):   e = Param['e']
    else:   e = 0.001
    if Param.has_key("ro"):  ro = Param["ro"]
    else:   ro = np.ones((1,c))

    X = Data['X']
    [N, n] = map(int, X.shape)

    f = np.zeros_like(X.T[0])
    f_new = np.zeros_like(f)
    d = np.zeros((N, c))
    v = np.zeros((c, n))
    # Initialize Cluster matrix randomly
    for i in range(c):
        v[i] = X[randint(0, N - 1)]
        while not v[np.where(v == v[i])].all():
            v[i] = X[randint(0, N - 1)]

    # Iterate
    run = 0
    while True and run != 20:
        # Calculate each points' belongings
        for i in range(c):
            d[:, i] = np.apply_along_axis(np.linalg.norm, 1, X - v[i])
        f_new = np.argmin(d, axis=1)
        # Calculate new medoids
        for i in range(c):
            clusterSize = np.size(d[np.where(f_new == i)]) / n
            if clusterSize:
                avg = np.average(X[np.where(f_new == i)], axis=0)
                tmp_d = np.zeros((clusterSize, 1))
                print np.apply_along_axis(np.linalg.norm, 1, X[np.where(f_new == i)] - avg)
                tmp_d = np.linalg.norm(X[np.where(f_new == i)] - avg, axis=1)
                v[i] = X[np.argmin(tmp_d)]
            else:
                v[i] = X[0]
        if np.linalg.norm(f - f_new) < e:
            break  # If the distance between current partition vector (f_new) and previously iterated p. vector (f) is under terminate tolerance, halt
        f = np.copy(f_new)
        run += 1

    result = {"Data": {"d": d, "f": f}, "Cluster": {"v": v}, "iter": run, "cost": 0}

    # plot, show results
    if Param.vis:
        colors = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 1, 1), (1, 0, 1), (1, 1, 0), (1, 1, 1)]
        fig = plt.figure("KMedoid - " + str(c) + " clusters")
        adat = fig.add_subplot(111, projection='3d')
        adat.set_xlabel("x tengely")
        adat.set_ylabel("y tengely")
        adat.set_zlabel("z tengely")
        for i in range(N):
            adat.scatter(X[i][0], X[i][1], X[i][2], c=colors[f[i]])
        for i in range(c):
            adat.scatter(v[i][0], v[i][1], v[i][2], c=colors[i], s=400)
        plt.show()

    return result
