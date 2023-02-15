
"""
Generates random graphs with varying degrees and runs EdgeGen. Computes errors.

"""
import sys
import numpy as np
import pandas as pd 
import subprocess
from genGraph_maxDegree import GenRandomGraph_maxdegree
from test_oracle_parallel import oracle_parallel
from test_oracle_single import oracle_single
from EdgeGen import EdgeGen
split_dic = lambda txt_ii : [ int(txii) for txii in txt_ii.split('_') ] 



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


#%%
min_V = 5
max_V = 10
tot_dif_var = (max_V - min_V)+1
num_rep = 25

for max_degree in [2,3,4,5]:
    EDGEGEN_time = np.zeros((num_rep,tot_dif_var), dtype = float)
    EDGEGEN_time_cont = np.zeros((num_rep,tot_dif_var), dtype = float)
    ASP_oldsat_time = np.zeros((num_rep,tot_dif_var), dtype = float)
    ASP_newsat_time = np.zeros((num_rep,tot_dif_var), dtype = float)
    SAT_time = np.zeros((num_rep,tot_dif_var), dtype = float)

    tot_num_iter = np.zeros((num_rep,tot_dif_var), dtype = int)
    var_enum = -1
    for noVer in range(min_V,max_V+1,2):
      var_enum = var_enum +1
     
      for iteration in range(num_rep):
        
        [D_true, E_true, dum_verts]  = GenRandomGraph_maxdegree(noVer,max_degree)
        
        if noVer < 16:
            subprocess.call ("Rscript --vanilla ../ASP_run/hyttinen2014uai_ver6/pkg/run_test_satisfy.R %d"%noVer, shell=True)
            this_ASP_oldsat_time = np.loadtxt('../ASP_run/hyttinen2014uai_ver6/pkg/R/solving_time_oldsat.txt').tolist()
            ASP_oldsat_time[iteration, var_enum] = this_ASP_oldsat_time
            
            
            subprocess.call ("Rscript --vanilla ../ASP_run_newASP/hyttinen2014uai_ver6/pkg/run_test_satisfy.R %d"%noVer, shell=True)
            this_ASP_newsat_time = np.loadtxt('../ASP_run_newASP/hyttinen2014uai_ver6/pkg/R/solving_time_newsat.txt').tolist()
            ASP_newsat_time[iteration, var_enum] = this_ASP_newsat_time
          
            S, C = oracle_single(noVer)
            
        else:
            S, C = oracle_parallel(noVer)
            this_ASP_oldsat = 0
            
       
        
        
        this_edgegen_time = EdgeGen(noVer,S,C)
        EDGEGEN_time[iteration, var_enum] = this_edgegen_time

        
        
        
        
        
        



