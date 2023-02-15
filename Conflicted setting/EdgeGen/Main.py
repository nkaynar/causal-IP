
"""
Generates random graphs with varying degrees and runs EdgeGen. Computes errors.

"""


import numpy as np
import pandas as pd
from test_conflicted import conflicted_indep
from true_IPerror import computeIPerror
from EdgeGen import EdgeGen
from ASP_results import conflicted_ASP
from getError import computeError
from genGraph_maxDegree import GenRandomGraph_maxdegree
import sys
import pdb


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


def dic_merger(d1,d2):
    d_merged = d1.copy()
    for this_key in d2.keys():
        if this_key in d_merged.keys():
            d_merged[this_key].extend(d2[this_key])
        else:
            d_merged[this_key] = d2[this_key]
    return(d_merged)


#%%
min_V = 5
max_V = 10
tot_dif_var = (max_V - min_V)+1
num_rep = 25

for max_degree in [2,3,4,5]:
    alg_time = np.zeros((num_rep,tot_dif_var), dtype = float)
    alg_error = np.zeros((num_rep,tot_dif_var), dtype = float)
    alg_loss = np.zeros((num_rep,tot_dif_var), dtype = float)
    alg_weighted_loss = np.zeros((num_rep,tot_dif_var), dtype = float)
    
    
    
    
    ASP_newsat_time = np.zeros((num_rep,tot_dif_var), dtype = float)
    ASP_newsat_error = np.zeros((num_rep,tot_dif_var), dtype = float)
    ASP_newsat_loss = np.zeros((num_rep,tot_dif_var), dtype = float)
    ASP_weighted_loss = np.zeros((num_rep,tot_dif_var), dtype = float)
    
    error_on_indep = np.zeros((num_rep,tot_dif_var), dtype = float)
    tot_test_weight = np.zeros((num_rep,tot_dif_var), dtype = float)
    
    
    tot_num_iter = np.zeros((num_rep,tot_dif_var), dtype = int)
    var_enum = -1

    
    for noVer in range(min_V,max_V+1):
      var_enum = var_enum + 1 
          
      for iteration in range(num_rep):
        [D_true, E_true, dum_verts]  = GenRandomGraph_maxdegree(noVer,max_degree)
        
        previous_graph_edge_indices_S_violated = []
        previous_graph_edge_indices_C_not_satisfied = []
        
        
        if noVer<15: 
           
            
            ASP_error,this_obj_ASP,this_ASP,S_true_asp, C_true_asp,D_true_asp,E_true_asp,D_est_asp,E_est_asp,true_ASP_loss,weighted_ASP_loss = conflicted_ASP(noVer)
    
            ASP_newsat_time[iteration, var_enum] = this_ASP
            ASP_newsat_loss[iteration, var_enum] = true_ASP_loss
            ASP_newsat_error[iteration, var_enum] = ASP_error
            ASP_weighted_loss[iteration, var_enum] = weighted_ASP_loss
            S,C,w_s,w_c = conflicted_indep(noVer)                    
            
            
        else:
           S_true_asp, C_true_asp, D_true_asp,E_true_asp = conflicted_ASP(noVer)
           S,C,w_s,w_c = conflicted_indep(noVer)
            
            
    
        
        tot_test_weight[iteration, var_enum] = sum([sum(ww) for ww in w_s.values()])+sum([sum(ww) for ww in w_c.values()])
        prob_error = computeError(S_true_asp,C_true_asp,S, C)
        error_on_indep[iteration, var_enum] = prob_error
        
    
    
        this_edgegen_time,D_est_int,E_est_int,S_violated_o, C_not_yet_satisfied_o,all_errors_vals,previous_graph_edge_indices = EdgeGen(noVer,S,C,w_s,w_c)
        minIndex = all_errors_vals.index(min(all_errors_vals))
        
        
        edges_found_index = previous_graph_edge_indices[minIndex]
        
        all_edges = []
        for node1 in range(noVer):    
             for node2 in range(noVer):
                 if node1<node2:
                     for edge_dir in [-1, -2, -3]:
                         all_edges.append([node1, edge_dir, node2])  
                         
        
        D_est = np.zeros((noVer,noVer),dtype=int)
        E_est = np.zeros((noVer,noVer),dtype=int)
        
        for e in edges_found_index:
            this_edge_info = all_edges[e]  
            if not this_edge_info[1]==-3: 
                if D_est[this_edge_info[0], this_edge_info[2]]==0:                             
                    D_est[this_edge_info[0], this_edge_info[2]] = this_edge_info[1]
                else:
                    D_est[this_edge_info[0], this_edge_info[2]] = -3
            else: # if -3 then confounder
                E_est[this_edge_info[0], this_edge_info[2]] = -1
            
                
        # If i --->j is present, then the type of edge between i and j is --> (-1) and the type of edge between
        # j and i is <--- (-2).
        # Complete D_true considering above observation
        for ii in range(noVer):
            for ii_2 in range(noVer):
                if D_est[ii,ii_2]==-1:
                    D_est[ii_2,ii]=-2
                if D_est[ii,ii_2]==-2:
                    D_est[ii_2,ii]=-1
                if D_est[ii,ii_2]==-3:
                    D_est[ii_2,ii]=-3
                    
        for ii in range(noVer):
            for ii_2 in range(noVer):
                if E_est[ii,ii_2]==-1:
                    E_est[ii_2,ii]=-1
        
        for this_edge_ind in edges_found_index:
            this_Edge = all_edges[this_edge_ind]
            
            
        IPloss = computeIPerror(D_est, E_est,S,C,noVer)
        IPerror = computeIPerror(D_est, E_est,S_true_asp,C_true_asp,noVer)
        print(IPerror)
        
        alg_time[iteration, var_enum] = this_edgegen_time
        alg_error[iteration, var_enum] = IPerror
        alg_loss[iteration, var_enum] = IPloss
        alg_weighted_loss[iteration, var_enum] = min(all_errors_vals)
        
        sys.exit()
            
            
            
            
            
            
            
        
        
        
        



