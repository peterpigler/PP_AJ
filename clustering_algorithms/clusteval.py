# -*- coding: utf-8 -*-
"""
@Clusteval

@author: Peter Pigler
"""
import numpy as np
from math import sqrt


def clusteval(New, Result, Param):


    # load Parameters
    v = Result["Cluster"]['V']
    c = Param['c']
    if Param.has_key('m'): m = Param['m']
    else: m = 2
    X = New.X
    [N, n] = map(int, X.shape)
    d = np.zeros((N, c))
    f0 = np.zeros_like(d)

    # Determine whether GK, GG or FCM
    if Result["Cluster"].has_key('Pi'): # GGclust
        A = Result["Cluster"]['P']
        f0 = Result["Data"]['f']
        fm = pow(f0,m)
        Pi = 1.0 / N * fm.sum(axis=0)
        for i in range(c):
            Xv = X - v[i]
            Xf = np.multiply(Xv, fm.T[i][:, np.newaxis])
            aaa = 1.0/(pow(np.linalg.det(np.linalg.pinv(A[i])),1.0/2.0))
            bbb = 1.0/Pi[i]
            ccc = 1./2.*np.sum(np.multiply(np.dot(Xv,np.linalg.pinv(A[i])),Xv),axis = 1)
            ddd = np.multiply(np.dot(Xv,np.linalg.pinv(A[i])),Xv)
            # d[:,i] = 1.0/(pow(np.linalg.det(np.linalg.pinv(P[i])),1.0/2.0))*1.0/Pi[i]*np.exp(1./2.*np.sum(np.multiply(np.dot(Xv,np.linalg.pinv(P[i])),Xv),axis = 1))
            d[:,i] = aaa*bbb*np.exp(ccc)
        for i in range(N):
            tmp = d[i]  # Create a Distance matrix from D[i] 1-D vector
            tmp = np.repeat(tmp, c)
            tmp = tmp.reshape((c, c))
            f0[i] = 1.0 / np.dot(pow(tmp, 2.0 / (m - 1)), pow(1.0 / d[i], 2.0 / (m - 1)))

    elif Result["Cluster"].has_key('P'):    # GK
        print "GK"
        P = np.zeros((c, n, n))
        for i in range(c):
            d[:, i] = np.apply_along_axis(np.linalg.norm, 1, X - v[i])
        for i in range(N):
            tmp = d[i]  # Create a Distance matrix from d[i] 1-D vector
            tmp = np.repeat(tmp, c)
            tmp = tmp.reshape((c, c))
            f0[i] = 1.0 / np.dot(pow(tmp, 2.0 / (m - 1)), pow(1.0 / d[i], 2.0 / (m - 1)))
        fm = pow(f0, m)
        for i in range(c):
            Xf = X - v[i]
            Xf = np.multiply(Xf, fm.T[i][:, np.newaxis])
            P[i] = np.cov(Xf.T)
        for i in range(c):
            A = np.dot(pow(np.linalg.det(P[i]), 1.0 / n), np.linalg.inv(P[i]))
            for j in range(N):
                d[j, i] = sqrt(np.dot((np.dot((X[j] - v[i]), A)), X[j] - v[i]))

    else:   # FCM
        d =np.zeros((N, c))
        for i in range(c):
            d[:, i] = np.apply_along_axis(np.linalg.norm, 1, X - v[i])
        for i in range(N):
            tmp = d[i]  # Create a Distance matrix from d[i] 1-D vector
            tmp = np.repeat(tmp, c)
            tmp = tmp.reshape((c, c))
            f0[i] = 1.0 / np.dot(pow(tmp, 2.0 / (m - 1)), pow(1.0 / d[i], 2.0 / (m - 1)))

    eval = {'d' : d, 'f' : f0}

    return eval