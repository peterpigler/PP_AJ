# -*- coding: utf-8 -*-
"""
@GKclust

@author: Peter Pigler
"""
import numpy as np
from random import randint
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from math import sqrt
import Param
import Data


def gkclust(Data, Param):

    if  'c' in dir(Param):  c = Param.c
    else:   c = 6
    if 'm' in dir(Param):   m = Param.m
    else:   m = 2
    if 'e' in dir(Param):   e = Param.e
    else:   e = 0.001
    if "ro" in dir(Param):  ro = Param.e
    else:   ro = np.ones((1,c))


    X = Data.X
    [N, n] = map(int, X.shape)

    f = np.zeros((N, c))
    f_new = np.zeros_like(f)
    d = np.zeros_like(f)
    v = np.zeros((c, n))
    # Initialize Partition matrix randomly
    for i in range(N):
        f[i][randint(0, c - 1)] = 1
    run = 0
    while True and (run != 20):
        fm = pow(f, m)
        # Calculate cluster prototypes:
        for i in range(c):
            v[i] = np.average(X, axis=0, weights=fm.T[i])

        # Calculate the cluster covariance matrices
        P = np.zeros((c, n, n))
        for i in range(c):
            Xf = X - v[i]
            Xf = np.multiply(Xf, fm.T[i][:, np.newaxis])
            P[i] = np.cov(Xf.T)

        # Calculate the distances:
        for i in range(c):
            A = np.dot(pow(np.linalg.det(P[i]), 1.0 / n), np.linalg.inv(P[i]))
            for j in range(N):
                d[j, i] = sqrt(np.dot((np.dot((X[j] - v[i]), A)), X[j] - v[i]))

        # Update the partition matrix:
        for i in range(N):
            tmp = d[i]
            tmp = np.repeat(tmp, c)
            tmp = tmp.reshape((c, c))
            f_new[i] = 1.0 / np.dot(pow(tmp, 2.0 / (m - 1)), pow(1.0 / d[i], 2.0 / (m - 1)))

        if np.linalg.norm(f - f_new) < e:
            break
        f = np.copy(f_new)
        run += 1

    fm = pow(f_new,m)
    P = np.zeros((c, n, n))
    M = np.copy(P)
    V = np.zeros((c,n))
    D = np.copy(V)

    for i in range(c):
        Xf = X - v[i]
        Xf = np.multiply(Xf, fm.T[i][:, np.newaxis])
        P[i] = np.cov(Xf.T)

        ev, ed = np.linalg.eig(P[i])
        V[i] = ev
        D[i] = np.diag(ed)

    result = {"Data": {"d": d, "f": f}, "Cluster": {"v": v, "P": P, "M": M, "V": V, "D": D}, "iter": run, "cost": 0}

    # Plot
    if Param.vis:
        fig = plt.figure("GKclust - " + str(c) + " clusters")
        adat = fig.add_subplot(111, projection='3d')
        adat.set_xlabel("Axis X")
        adat.set_ylabel("Axis Y")
        adat.set_zlabel("Axis Z")
        for i in range(N):
            adat.scatter(X[i][0], X[i][1], X[i][2], c=tuple(f[i]), s=80)
        for i in range(c):
            adat.scatter(v[i][0], v[i][1], v[i][2], s=300, alpha=0.6, c="white")
        plt.show()


gkclust(Data, Param)
