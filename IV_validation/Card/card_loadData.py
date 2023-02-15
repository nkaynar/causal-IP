#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 25 16:01:45 2022

@author: sk2739
"""

import random
import numpy as np
import pandas as pd
import pingouin as pg
from itertools import combinations
from tqdm import tqdm
import sys
import json 
import matplotlib.pyplot as plt
import pdb
from sklearn.utils import shuffle,resample
import math
from scipy import stats
from operator import add





data_df = pd.read_excel('card.xls', header=None)
data_df = data_df[data_df[5].notna()]
data_df = data_df[data_df[6].notna()]
data_df = data_df.replace('.', np.nan)
data_df =  data_df.dropna() 
data_weigths = data_df[7]
data_weigths.to_csv('card_weigths.csv',index = False)




#pdb.set_trace()
# parent_edu = list( map(add,  data_df[5].tolist(),  data_df[6].tolist()) )
# parent_edu = [ii/2 for ii in parent_edu]
# data_df['parent'] = parent_edu
# data_df['prox_agg'] = list(np.maximum(data_df[1].tolist(),data_df[2].tolist()))


use_columns = [2,3,20,24,25,21]
data_df = data_df.filter(use_columns)




data_df.columns = ['prox','edu','south66','smsa66','wage','race']


data_df.to_csv('card_CD.csv',index = False)

