"""
Compute total errors among two sets of conditional independence/dependence relations.

"""



import os
import random
import pandas as pd
#import copy
import sys
#import itertools
import numpy as np
from itertools import combinations 
#import itertools
#from numpy import ndarray
from gurobipy import *
import subprocess
import json
def computeError(S1,C1,S2,C2):
    
     true_conflicts = 0
     for this_key in S1.keys():
         true_separators = S1[this_key]
         if this_key in S2.keys():
             estimated_separators = S2[this_key]
             for this_s in true_separators:
                 if this_s not in estimated_separators:
                     true_conflicts = true_conflicts+1
         else:
             true_conflicts = true_conflicts+len(true_separators)
            
     for this_key in C1.keys():
         true_connectors = C1[this_key]
         if this_key in C2.keys():
             estimated_connectors= C2[this_key]
             for this_c in true_connectors:
                 if this_c not in estimated_connectors:
                     true_conflicts = true_conflicts+1
         else:
             true_conflicts = true_conflicts+len(true_connectors)
             
     return(true_conflicts)
            
