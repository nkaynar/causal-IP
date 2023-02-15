#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Construct a bootstrap sample
"""

import pandas
from sklearn.utils import shuffle,resample
from random import sample
import random
import pdb
import numpy as np

def bootstrap_school(i_run):
    data_df = pandas.read_csv('card_CD.csv')
    weigths_df = pandas.read_csv('card_weigths.csv')
    this_data_df = data_df.sample(1600, replace = True , weights =weigths_df.values.ravel())
    this_data_df.to_csv('../ASP_schoolData_logweights/hyttinen2014uai_ver6/pkg/R/data_bootstrap.csv',index=False, header = False)
    