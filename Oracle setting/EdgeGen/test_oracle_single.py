
"""
oracle results
"""

from itertools import combinations 
import os
import numpy as np
import subprocess
import json
import timeit


def ordered(a):
    
    if a[2]<a[0]:
        if a[1]==-1:
            i_1 = a[2]
            i_2 = -2
            i_3 = a[0]
        if a[1]==-2:
            i_1 = a[2]
            i_2 = -1
            i_3 = a[0]
        if a[1]==-3:
            i_1 = a[2]
            i_2 = -3
            i_3 = a[0]
    else:
        i_1 = a[0]
        i_2 = a[1]
        i_3 = a[2]
        
    return([i_1,i_2,i_3])





def oracle_single(noVer):
    S_all = {}
    C_all = {}
    
    #ONLY READS EXPORT.JSON
    #%%    
    with open('../ASP_run/hyttinen2014uai_ver6/pkg/R/export.JSON') as f:
         data = json.load(f)
         
         for ii in range(len(data)):
             this_nodes = data[ii]['vars']
             this_key = '%s_%s'%(this_nodes[0]-1 ,this_nodes[1]-1)
             this_c = data[ii]['C']
             if not isinstance(this_c, list):
                 this_c = [this_c]
             if list(data[ii]['independent'].values())[0]:
             #if data[ii]['independent']:
                 if this_key in S_all.keys():
                     S_all[this_key].append([x - 1 for x in this_c])
                 else:
                     S_all[this_key] = [[x - 1 for x in this_c]]
             else:
                 if this_key in C_all.keys():
                     C_all[this_key].append([x - 1 for x in this_c])
                 else:
                     C_all[this_key] = [[x - 1 for x in this_c]]       
 
    
    #%%  
    S_all_sorted =  {}
    C_all_sorted = {}
    
    for this_key in S_all.keys():
        for length in range(len(max(S_all[this_key],key=len))+1):
           s_subset = [this_c for this_c in S_all[this_key] if len(this_c)==length]  
           s_subset = sorted(s_subset)
           if this_key in S_all_sorted.keys():
               S_all_sorted[this_key].extend(s_subset)
           else:
               S_all_sorted[this_key] = s_subset
               
               
    for this_key in C_all.keys():
        for length in range(len(max(C_all[this_key],key=len))+1):
           s_subset = [this_c for this_c in C_all[this_key] if len(this_c)==length]  
           s_subset = sorted(s_subset)
           if this_key in C_all_sorted.keys():
               C_all_sorted[this_key].extend(s_subset)
           else:
               C_all_sorted[this_key] = s_subset        
               
    S = S_all_sorted
    C = C_all_sorted
    
  
    
    return(S,C)
