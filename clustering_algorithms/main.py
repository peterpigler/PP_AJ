# -*- coding: utf-8 -*-
"""
@GGClust

@author: Peter Pigler
"""

import init

Data = init.data
Param = init.param

from gathgeva import ggclust
from gustafsonkessel import gkclust
from fuzzycmeans import fcmclust

FCM = fcmclust(Data, Param)
Data['d'] =  FCM["Data"]['d']
Data['v'] = FCM["Cluster"]['v']
Data['f'] = FCM["Data"]['f']
GKclust = gkclust(Data, Param)
Data['d'] =  GKclust["Data"]['d']
Data['v'] = GKclust["Cluster"]['v']
Data['f'] = GKclust["Data"]['f']
Data['P'] = GKclust["Cluster"]['P']
Data['M'] = GKclust["Cluster"]['M']
Data['V'] = GKclust["Cluster"]['V']
Data['D'] = GKclust["Cluster"]['D']
GGclust = ggclust(Data, Param)




# GGclust = ggclust(Data, Param)


