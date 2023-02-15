
"""
Construct a bootstrap sample

"""

import pandas
from sklearn.utils import shuffle,resample
from random import sample
import random

def bootstrap_school(i_run):
    data_df = pandas.read_csv('QOB_working.csv')
    this_data_df = resample(data_df,replace=True,random_state=None)
    this_data_df.to_csv('../ASP_schoolData_logweights/hyttinen2014uai_ver6/pkg/R/data_bootstrap.csv',index=False)
    