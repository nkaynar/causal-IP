
"""
Bootstrap main loop

"""


import math
import numpy as np
from test_conflicted import conflicted_indep
from EdgeGen import EdgeGen
from bootstrap_school import bootstrap_school
from functools import reduce
import numpy.ma as ma
from edge_connected_info_limLength_IV import con_edge_disc_lim


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
noVer = 6
vertices = list(range(noVer))
all_edges = []
for node1 in range(noVer):    
      for node2 in range(noVer):
          if node1<node2:
              for edge_dir in [-1, -2, -3]:
                  all_edges.append([node1, edge_dir, node2])  
                
edge_freq = np.zeros((1,len(all_edges)))
edge_freq_IV = np.zeros((1,len(all_edges)))
difference = []
all_posterior = []
all_posterior_IV = []
sum_satisfied_weights = []
sum_satisfied_weights_IV = []
sum_error_weights = []
sum_error_weights_IV = []
sum_difference = []



for iteration in range(1):
    # Bootstrap sampling
    bootstrap_school(iteration)
    # get independence/dependence relations
    S,C,w_s,w_c = conflicted_indep(noVer)   
    
    
    # unrestricted model space
    S_violated_all_unr,C_not_yet_satisfied_all_unr,this_edgegen_time,all_errors_vals,previous_graph_edge_indices,error_weights,satisfied_weigths = EdgeGen(noVer,S,C,w_s,w_c,0,[],())
    
    all_errors_vals = np.array(all_errors_vals)
    minIndex = np.argmin(ma.masked_where(all_errors_vals==0, all_errors_vals)) 
    posterior = reduce(lambda x, y: x*y, [math.exp(t_p) for t_p in satisfied_weigths[minIndex]])
    all_posterior.append(posterior)
    sum_satisfied_weights.append(sum(satisfied_weigths[minIndex]))
    sum_error_weights.append(sum(error_weights[minIndex]))

        
    edges_found_index = previous_graph_edge_indices[minIndex]
    edge_found = []
    for t_e in edges_found_index:
        edge_freq[0,t_e] = edge_freq[0,t_e]+1
        edge_found.append(all_edges[t_e])
       
       
    D_est = np.zeros((noVer,noVer),dtype=int)
    E_est = np.zeros((noVer,noVer),dtype=int)
   
    for i in range(noVer):
        for j in range(i, noVer):
            if ordered([i,-3,j]) in edge_found:
                E_est[i,j] = -1
                E_est[j,i] = -1
            if ordered([i,-1,j]) in edge_found and ordered([i,-2,j]) in edge_found:
                D_est[i,j] = -3
                D_est[j,i] = -3
               
            elif ordered([i,-1,j]) in edge_found:
                D_est[i,j] = -1
                D_est[j,i] = -2
            elif ordered([i,-2,j]) in edge_found:
                D_est[i,j] = -2
                D_est[j,i] = -1
               
    dum_verts_int_all = []
    for ii in vertices:
        add_verts = []
        for jj in vertices:
            if D_est[ii,jj]!=0 or E_est[ii,jj]!=0:
                add_verts.append(jj)
        dum_verts_int_all.append(add_verts)
                       
       
   
    # IV is enforced
    path_con_lim,path_edge_lim,path_length_lim,path_IV_violater = con_edge_disc_lim(D_est,E_est, dum_verts_int_all, noVer,noVer-1 ) 
    uncond_violate = 0
    for this_v in path_IV_violater.values():
        if 1 in this_v:
            uncond_violate = 1

    if uncond_violate == 0 and len(set(edges_found_index).intersection(set([6,7,8])))>0:
        
        edges_found_index_IV = edges_found_index
        sum_satisfied_weights_IV.append(sum(satisfied_weigths[minIndex]))
        sum_error_weights_IV.append(sum(error_weights[minIndex]))        
        for t_e in edges_found_index_IV:
            edge_freq_IV[0,t_e] = edge_freq_IV[0,t_e]+1
            
    else:        
        condset1 = ()
        S_violated_all_IV,C_not_yet_satisfied_all_IV,this_edgegen_time_IV, all_errors_vals_IV, previous_graph_edge_indices_IV, error_weights_IV, satisfied_weigths_IV = EdgeGen(noVer,S,C,w_s,w_c,1,[],condset1)
        all_errors_vals_IV = np.array(all_errors_vals_IV)
        minIndex_IV = np.argmin(ma.masked_where(all_errors_vals_IV==0, all_errors_vals_IV)) 
        posterior_IV = reduce(lambda x, y: x*y, [math.exp(t_p) for t_p in satisfied_weigths_IV[minIndex_IV]])
        all_posterior_IV.append(posterior_IV)
        sum_satisfied_weights_IV.append(sum(satisfied_weigths_IV[minIndex_IV]))
        sum_error_weights_IV.append(sum(error_weights_IV[minIndex_IV]))
        
        
        edges_found_index_IV = previous_graph_edge_indices_IV[minIndex_IV]
        
        edges_found_index_IV_strt = np.zeros((len(all_edges,)))
        for t_e in edges_found_index_IV:
            edges_found_index_IV_strt[t_e] = 1
        
        for t_e in edges_found_index_IV:
            edge_freq_IV[0,t_e] = edge_freq_IV[0,t_e]+1
        

        
    sum_difference.append(sum(error_weights[minIndex]) - sum_error_weights_IV[-1])
    
 
            
            
            
        
        
        
        



