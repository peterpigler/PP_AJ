import numpy as np
import os.path

n = 3

if os.path.isfile("iris.csv"):
    try:
        class Data:
            def __init__(self):
                pass

            X = np.loadtxt("iris.csv",delimiter=',', dtype=float, usecols=tuple(range(n)))
            Xold = np.copy(X)
            min = np.min(X, axis = 0)
            max = np.max(X, axis = 0)
            mean = np.mean(X, axis = 0)
            std = np.std(X, axis = 0)
    except:
        print "File found but error while loading data"
else:
    print "File not found"
