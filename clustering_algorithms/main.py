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
GKclust = gkclust(Data, Param)
GGclust = ggclust(Data, Param)
