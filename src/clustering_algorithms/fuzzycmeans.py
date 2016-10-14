# -*- coding: utf-8 -*-
"""
@FCMclust

@author: Peter Pigler
"""
import numpy as np
from random import randint
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


def fcmclust(Data, Param):


    if  Param.has_key('c'):  c = Param['c']
    else:   c = 3
    if Param.has_key('m'):   m = Param['m']
    else:   m = 2
    if Param.has_key('e'):   e = Param['e']
    else:   e = 0.001
    if Param.has_key("ro"):  ro = Param["ro"]
    else:   ro = np.ones((1,c))


    X = Data['X']
    [N, n] = map(int, X.shape)
    f = np.zeros((N, c))
    f_new = np.zeros_like(f)  # f partition matrix in next iteration
    d = np.zeros_like(f)
    v = np.zeros((c, n))
    # Initialize Partition matrix randomly
    for i in range(N):
        f[i][randint(0, c - 1)] = 1

    # Iterate
    run = 0
    while True and run != 20:
        # Calculate cluster prototypes:
        for i in range(c):
            # noinspection PyTypeChecker
            v[i] = np.average(X, axis=0, weights=pow(f.T[i], m))

        # Calculate the distances:
        for i in range(c):
            d[:, i] = np.apply_along_axis(np.linalg.norm, 1, X - v[i])

        # Update the partition matrix:
        for i in range(N):
            tmp = d[i]  # Create a Distance matrix from d[i] 1-D vector
            tmp = np.repeat(tmp, c)
            tmp = tmp.reshape((c, c))
            # noinspection PyTypeChecker,PyTypeChecker
            f_new[i] = 1.0 / np.dot(pow(tmp, 2.0 / (m - 1)), pow(1.0 / d[i], 2.0 / (m - 1)))

        if np.linalg.norm(f - f_new) < e:
            break
        f = np.copy(f_new)
        run += 1

    result = {"Data": {"d": d, "f": f}, "Cluster": {"v": v}, "iter": run, "cost": 0}

    # Plot
    if Param["vis"]:
        fig = plt.figure("FCMclust - " + str(c) + " clusters")
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
