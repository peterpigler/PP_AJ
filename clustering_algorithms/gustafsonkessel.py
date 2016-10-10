# -*- coding: utf-8 -*-
"""
@GKclust

@author: Peter Pigler
"""
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from math import sqrt


def gkclust(Data, Param):


    # Checking if the parameters are given
    if Param.has_key('c'):  c = Param['c']
    else:   c = 3
    if Param.has_key('m'):   m = Param['m']
    else:   m = 2
    if Param.has_key('e'):   e = Param['e']
    else:   e = 0.001
    if Param.has_key("ro"):  ro = Param["ro"]
    else:   ro = np.ones((1,c))
    if Param.has_key("gamma") : gamma = Param["gamma"]
    else:   gamma = 0
    if Param.has_key("beta"): beta = Param["beta"]
    else:   beta = 1e15;

    X = Data['X']
    [N, n] = map(int, X.shape)

    f_new = np.zeros((N, c))
    f = np.copy(f_new)
    d = np.zeros_like(f)
    v = np.zeros((c, n))

    # Checking if cluster parameters are given
    if Data.has_key('v'):
        v = Data['v']
        if Data.has_key('d'):
            d = Data['d']
        else:
            # Initialize distance matrix
            for i in range(c):
                d[:, i] = np.apply_along_axis(np.linalg.norm, 1, X - v[i])
    else:
        # Initialize clusters
        mM = np.max(X, axis=0)
        mm = np.min(X, axis=0)
        v = ((mM - mm) * np.random.random_sample(c, n)) + mm
    if Data.has_key('f'):
        f = Data['f']
    else:
        for i in range(N):
            tmp = d[i]  # Create a Distance matrix from d[i] 1-D vector
            tmp = np.repeat(tmp, c)
            tmp = tmp.reshape((c, c))
            f[i] = 1.0 / np.dot(pow(tmp, 2.0 / (m - 1)), pow(1.0 / d[i], 2.0 / (m - 1)))

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
    V = np.zeros((c,n))
    D = np.copy(V)

    for i in range(c):
        Xf = X - v[i]
        Xf = np.multiply(Xf, fm.T[i][:, np.newaxis])
        P[i] = np.cov(Xf.T)

        ev, ed = np.linalg.eig(P[i])
        V[i] = ev
        D[i] = np.diag(ed)

    # result outputs
    result = {"Data": {"d": d, "f": f}, "Cluster": {"v": v, "P": P, "V": V, "D": D}, "iter": run, "cost": 0}

    # Plot
    if Param["vis"]:
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

    return result
