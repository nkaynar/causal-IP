


"""
Algorithm 2: G-Postprocess sub-algorithm
"""


import sys
import numpy as np

import timeit
from itertools import combinations 

import multiprocessing as mp
from tqdm import tqdm


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


import pdb

def graph_postprocess(S, C, C_not_yet_satisfied, D_est_int,E_est_int, dum_verts_int, noVer):
    
    pairs = list(combinations(range(noVer),2))

    vertices = list(map(np.uint8,list(range(noVer))))
    
    for ii in vertices:
        for jj in vertices:
            if ii in dum_verts_int[jj]:
                dum_verts_int[ii].append(jj)
        dum_verts_int[ii] = list(set((dum_verts_int[ii]))) 
        
    graph = dict(zip(vertices,dum_verts_int))   
            
    C_not_yet_satisfied_2 = C_not_yet_satisfied.copy() 
    
    S_violated = {}    
    for i in range(noVer):
         for j in range(i+1,noVer):
             S_violated['%s_%s'%(i,j)] = []
             if '%s_%s'%(i,j) not in S.keys():
                 S['%s_%s'%(i,j)] = []
             if '%s_%s'%(i,j) not in C_not_yet_satisfied_2.keys():
                 C_not_yet_satisfied_2['%s_%s'%(i,j)] = []
            
    all_edges = []
    for node1 in vertices:    
         for node2 in vertices:
             if node1<node2:
                 for edge_dir in [-1, -2, -3]:
                     all_edges.append([node1, edge_dir, node2])  
                 



    from Edge_connected_class_V7 import conedge_compute_pairs
    
    S_keys = list(S.keys())
    C_not_yet_satisfied_2_keys = list(C_not_yet_satisfied_2.keys())
    
    var_list = []
    for (i,j) in pairs:
        pair_ij = f'{i}_{j}'
    
        S_ij = S[pair_ij]
        C_not_yet_satisfied_2_ij = C_not_yet_satisfied_2[pair_ij]
        S_violated_ij = S_violated[pair_ij]
    
        var_list.append([i,j, noVer, S_keys, S_ij, C_not_yet_satisfied_2_keys, C_not_yet_satisfied_2_ij,
                                D_est_int, E_est_int, vertices, graph, S_violated_ij, all_edges] )
    
    # aa = conedge_compute_pairs(var_list[0])
    
    tic = timeit.default_timer() 
    with mp.Pool(mp.cpu_count()) as pool:
        mp_it = pool.imap(conedge_compute_pairs, var_list)
        results = list(tqdm(mp_it, total=len(var_list) ))
        
    print('Time:', timeit.default_timer() - tic )     
    
    
  
    #%% Combine outputs [results from mp.Pool above]
    path_dir_index = {}
    path_col_index = {}
    path_collider = {}
    path_noncollider = {}
    path_des_req = {}
    S_violated_final = {}
    C_not_yet_satisfied_final = {}

    
    pairs_use = []
    for num_pair in range(len(pairs)):
    
        if results[num_pair][0] is None:
            continue
    
        pairs_use.append(pairs[num_pair])
        path_dir_index.update(results[num_pair][0])
        path_col_index.update(results[num_pair][1])
        path_collider.update(results[num_pair][2])
        path_noncollider.update(results[num_pair][3])
        path_des_req.update(results[num_pair][4])
        S_violated_final.update(results[num_pair][5])
        C_not_yet_satisfied_final.update(results[num_pair][6])
      
        
    #%%
    
    from Edge_connected_class_V7 import conedge_des_compute_pairs
    
    S_keys = list(S.keys())
    C_not_yet_satisfied_final_keys = list(C_not_yet_satisfied_final.keys())
    
    var_list_des = []
    for (i,j) in pairs_use:
        pair_ij = f'{i}_{j}'
    
        S_ij = S[pair_ij]
        C_not_yet_satisfied_final_ij = C_not_yet_satisfied_final[pair_ij]
        S_violated_ij = S_violated_final[pair_ij]
        #pdb.set_trace()
        path_col_index_ij = path_col_index[pair_ij]
        path_collider_ij = path_collider[pair_ij]
        path_noncollider_ij = path_noncollider[pair_ij]
        path_des_req_ij = path_des_req[pair_ij]
    
    
        var_list_des.append([i,j, noVer, S_keys, S_ij, S_violated_ij, 
                         C_not_yet_satisfied_final_keys, C_not_yet_satisfied_final_ij,
                         D_est_int, vertices, path_col_index_ij, path_collider_ij, 
                         path_noncollider_ij, path_des_req_ij ] )
        
    # i_test = 0
    # test_new = conedge_des_compute_pairs(var_list_des[0])
    
    
    tic = timeit.default_timer() 
    with mp.Pool(mp.cpu_count()) as pool:
        mp_it = pool.imap(conedge_des_compute_pairs, var_list_des)
        results_des = list(tqdm(mp_it, total=len(var_list_des) ))
        
    print('Time:', timeit.default_timer() - tic )     
    
    S_violated_3 = {}
    C_not_yet_satisfied_3 = {}
    
    
    for num_pair in range(len(pairs_use)):
        S_violated_3.update(results_des[num_pair][0])
        C_not_yet_satisfied_3.update(results_des[num_pair][1])
        
        
    return (S_violated_3, C_not_yet_satisfied_3)
    
    