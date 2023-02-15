
"""
EdgeGen Algorithm

"""

import numpy as np


import random
import timeit
from Edge_IntProg import NewEdge_IntProg
from Triples_connected_in_both import generate_triples
from Triple_orient import update_triple_orientation
from Update_triples import update_triples
from Update_triples_random import update_triples_random
from edge_connected_info_limLength_IV import con_edge_disc_lim
from Search_IntProg_matrix  import MainintProg_searchmatrix
from f_graphPostprocess import graph_postprocess
split_dic = lambda txt_ii : [ int(txii) for txii in txt_ii.split('_') ] 
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


#%%

def EdgeGen(noVer,S,C,w_s,w_c,validIV,prev_sol_start,condset):
    
    S_violated_all = {}
    C_not_yet_satisfied_all = {}
    it_no = 0  
    
    now_return = 0 
    comp_return = 0
    for t_k in C.keys():
        if t_k in S.keys() and S[t_k]==[]:
            del S[t_k]

    all_errors = []  
    maxlength = 6
              
                     
    unused_edges = []
    for i in range(noVer):    
        for j in range(i+1,noVer):  
                for edge_dir in [-1, -2, -3]:
                    unused_edges.append([i, edge_dir, j])  
    
    

    tic_alg =   timeit.default_timer()  
    

    collider_triple_initial,noncollider_triple_initial, col_noncol_triple_initial,edges,no_edge,col_orient,noncol_orient,connected_orient,connected_pairs = generate_triples(noVer, S, C)
    #collider_triple_initial,noncollider_triple_initial, col_noncol_triple_initial,edges,no_edge,col_orient,noncol_orient,connected_orient,connected_pairs = generate_triples(noVer, S, C)
    collider_pairs = []
    for [i,j,k] in collider_triple_initial:
        if sorted([i,j]) not in collider_pairs:
            collider_pairs.append(sorted([i,j]))
        if sorted([j,k]) not in collider_pairs:
            collider_pairs.append(sorted([j,k]))
            
    noncollider_pairs = []
    for [i,j,k] in noncollider_triple_initial:
        if sorted([i,j]) not in noncollider_pairs:
            noncollider_pairs.append(sorted([i,j]))
        if sorted([j,k]) not in noncollider_pairs:
            noncollider_pairs.append(sorted([j,k]))
            
    col_noncol_pairs = []
    for [i,j,k] in col_noncol_triple_initial:
         if sorted([i,j]) not in col_noncol_pairs:
             col_noncol_pairs.append(sorted([i,j]))
         if sorted([j,k]) not in col_noncol_pairs:
             col_noncol_pairs.append(sorted([j,k]))
     
     
    
    all_in_pairs = collider_pairs+noncollider_pairs+col_noncol_pairs
    
    edges_i = []
    new_edges_i = []
    for i in range(noVer):
        for j in range(i+1,noVer):
            if '%s_%s'%(i,j) not in S.keys() and sorted([i,j]) not in all_in_pairs:
                    edges_i.append([i,-1,j])
                    new_edges_i.append([i,-1,j])
                    #pdb.set_trace()
                                   

    previous_graph_edge_indices = []    
    edges = []
    #pdb.set_trace()
    new_edges, edges,g = NewEdge_IntProg(noVer,collider_triple_initial,noncollider_triple_initial,col_noncol_triple_initial,edges,col_orient,noncol_orient,connected_orient,noVer)
    new_edges.extend(new_edges_i)
    edges.extend(edges_i)
    

    
    for t_e in [[0,-1,1],[0,-2,1],[0,-3,1],[0,-1,3],[0,-2,3],[0,-3,3]]:
        if t_e not in edges:
            new_edges.append(t_e)
            edges.append(t_e)
    

            
    
    print(edges)
    initial_edges = edges.copy()
  
                                
    #construct D_est and E_est
    D_est = np.zeros((noVer,noVer),dtype=int)
    E_est = np.zeros((noVer,noVer),dtype=int)
    for i in range(noVer):
        for j in range(i, noVer):
            if ordered([i,-3,j]) in edges:
                E_est[i,j] = -1
                E_est[j,i] = -1
            if ordered([i,-1,j]) in edges and ordered([i,-2,j]) in edges:
                D_est[i,j] = -3
                D_est[j,i] = -3
                
            elif ordered([i,-1,j]) in edges:
                D_est[i,j] = -1
                D_est[j,i] = -2
                
            elif ordered([i,-2,j]) in edges:
                D_est[i,j] = -2
                D_est[j,i] = -1
       
           
                  
    vertices = list(range(noVer))
    dum_verts = []
    for ii in vertices:
        add_verts = []
        for jj in vertices:
            if D_est[ii,jj]!=0 or E_est[ii,jj]!=0:
                add_verts.append(jj)
        dum_verts.append(add_verts)
    
    path_con_lim,path_edge_lim,path_length_lim,path_IV_violater = con_edge_disc_lim(D_est,E_est, dum_verts, noVer,maxlength) 
    

    #pdb.set_trace()
    obj_val, runTime, C_not_yet_satisfied, C_not_yet_satisfied_ind, S_not_yet_satisfied, S_not_yet_satisfied_ind, D_est_int, E_est_int, dum_verts_int, edges_used_index, store_index, mod_status = MainintProg_searchmatrix(S, C,w_s,w_c, noVer, path_con_lim, path_edge_lim, path_length_lim, edges, prev_sol_start, 1-validIV, previous_graph_edge_indices,path_IV_violater,validIV,it_no)  
    obj_val_old = obj_val
        
    #pdb.set_trace()
    S_violated_o, C_not_yet_satisfied_o = graph_postprocess(S, C, C_not_yet_satisfied, D_est_int,E_est_int, dum_verts_int, noVer)  
    
    #pdb.set_trace()
    
    
    
    
    
    errors = 0
    error_weights_violated = []
    this_error_weigths_S = []
    this_error_weigths_C = []
    all_satisfied_weigths = []
    

    
    

    for this_kk in S_violated_o.keys():
        
        S_violated_o[this_kk] = [list(x) for x in set(tuple(x) for x in S_violated_o[this_kk])]
        unique_data = [list(x) for x in set(tuple(x) for x in S_violated_o[this_kk])]
        S_violated_ind = [S[this_kk].index(t_s_v) for t_s_v in unique_data]
        error_weights = [w_s[this_kk][this_kk_ind] for this_kk_ind in S_violated_ind]        
        this_error_weigths_S.extend(error_weights)
        errors = errors + sum(error_weights)
    
        
    for this_kk in C_not_yet_satisfied_o.keys():
        
        C_not_yet_satisfied_o[this_kk] = [list(x) for x in set(tuple(x) for x in C_not_yet_satisfied_o[this_kk])]
        unique_data = [list(x) for x in set(tuple(x) for x in C_not_yet_satisfied_o[this_kk])]
        C_not_yet_satisfied_ind = [C[this_kk].index(t_s_v) for t_s_v in unique_data]
        error_weights = [w_c[this_kk][this_kk_ind] for this_kk_ind in C_not_yet_satisfied_ind]
        this_error_weigths_C.extend(error_weights)
        errors = errors + sum(error_weights)
    
    
    num_ip = 0
    S_violated_all[num_ip] = S_violated_o
    C_not_yet_satisfied_all[num_ip] = C_not_yet_satisfied_o
    
    error_weights_violated.append(this_error_weigths_S+this_error_weigths_C)
    
    
    S_all_weigths = [a_weight_this for a_weight in w_s.values() for a_weight_this in a_weight]
    C_all_weigths = [a_weight_this for a_weight in w_c.values() for a_weight_this in a_weight]
    
    
    S_all_weigths = set(S_all_weigths).difference(set(this_error_weigths_S))
    C_all_weigths = set(C_all_weigths).difference(set(this_error_weigths_C))   
    
    satisfied_weigths = list(S_all_weigths) + list(C_all_weigths)      
    all_satisfied_weigths.append(satisfied_weigths)
    
    all_errors.append(errors)  
    
     
    previous_graph_edge_indices.append(store_index)
 
    toc_alg = timeit.default_timer() 
    tot_time = toc_alg - tic_alg
    
     
    added_rand_keys = []
    

    while tot_time<500:
        
        it_no = it_no +1                         
                       
        col_orient, noncol_orient, connected_orient = update_triple_orientation(collider_triple_initial, noncollider_triple_initial, col_noncol_triple_initial, col_orient, noncol_orient, connected_orient,edges)
        col_not, noncol_not,col_noncol_not = update_triples(C_not_yet_satisfied_o, collider_triple_initial, noncollider_triple_initial, col_noncol_triple_initial, col_orient, noncol_orient, connected_orient)

        
        if noncol_not!=[] or noncol_not!=[] or col_noncol_not!=[]:
            new_edges, edges,g = NewEdge_IntProg(noVer,col_not,noncol_not,col_noncol_not,edges,col_orient,noncol_orient,connected_orient,noVer)
            for t_e in [[0,-1,1],[0,-2,1],[0,-3,1],[0,-1,3],[0,-2,3],[0,-3,3]]:
                if t_e not in edges:
                    new_edges.append(t_e)
                    edges.append(t_e)
        else:
            
            col_not_r, noncol_not_r,col_noncol_not_r = update_triples_random(C_not_yet_satisfied_o, collider_triple_initial, noncollider_triple_initial, col_noncol_triple_initial, col_orient, noncol_orient, connected_orient)
            col_not = random.sample(col_not_r, min(1,len(col_not_r)))
            noncol_not = random.sample(noncol_not_r,min(1,len(noncol_not_r)))
            col_noncol_not = random.sample(col_noncol_not_r,min(1,len(col_noncol_not_r)))
            new_edges, edges,g = NewEdge_IntProg(noVer,col_not,noncol_not,col_noncol_not,edges,col_orient,noncol_orient,connected_orient,noVer)
            for t_e in [[0,-1,1],[0,-2,1],[0,-3,1],[0,-1,3],[0,-2,3],[0,-3,3]]:
                if t_e not in edges:
                    new_edges.append(t_e)
                    edges.append(t_e)
            
                            
        for this_new_edge in new_edges:                  
            unused_edges.remove(this_new_edge)  
            
        if new_edges == []:
            print(edges)
            if maxlength==noVer-1:

                C_n_S = {}
                C_n_S_length = {}
                for t_s_c in C.keys():
                    if t_s_c not in added_rand_keys:
                        [ii1,jj1] = split_dic(t_s_c)
                        if [ii1,-1,jj1] not in edges or [ii1,-2,jj1] not in edges or [ii1,-3,jj1] not in edges:
                            C_n_S[t_s_c] = C[t_s_c].copy()
                            C_n_S_length[t_s_c] = len(C[t_s_c])
                if C_n_S_length == {}:
                    now_return = 1
                
                else:                
                    e_key = max(C_n_S_length, key=C_n_S_length.get)
                    [ii,jj] = split_dic(e_key)                    
                    new_edges_all = [aa for aa in [[ii,-1,jj], [ii,-2,jj], [ii,-3,jj]] if aa not in edges]
                    new_edges = random.sample(new_edges_all,min(1,len(new_edges_all)))
                    
                    edges.extend(new_edges)
                    if new_edges_all == []:
                        added_rand_keys.append(e_key)
                    print(new_edges)
                     
               
                
            else:
          
                maxlength = min(maxlength +1,noVer-1)
                
                removed_keys_S = []
                for this_key in S.keys():
                    if S[this_key] == []:
                        removed_keys_S.append(this_key)
                for this_removed_key in removed_keys_S:
                    del S[this_removed_key]
                       
                       
                collider_triple,noncollider_triple, col_noncol_triple,edges,no_edge,col_orient,noncol_orient,connected_orient,connected_pairs = generate_triples(noVer, S, C)
                col_orient, noncol_orient, connected_orient = update_triple_orientation(collider_triple_initial, noncollider_triple_initial, col_noncol_triple_initial, col_orient, noncol_orient, connected_orient,edges)
                col_not, noncol_not,col_noncol_not = update_triples(C_not_yet_satisfied_o, collider_triple_initial, noncollider_triple_initial, col_noncol_triple_initial, col_orient, noncol_orient, connected_orient)
                
                
                if noncol_not!=[] or noncol_not!=[] or col_noncol_not!=[]:   
                    new_edges, edges,g = NewEdge_IntProg(noVer,col_not,noncol_not,col_noncol_not,edges,col_orient,noncol_orient,connected_orient,noVer)
                
                
                else:
                    
                    col_not_r, noncol_not_r,col_noncol_not_r = update_triples_random(C_not_yet_satisfied_o, collider_triple_initial, noncollider_triple_initial, col_noncol_triple_initial, col_orient, noncol_orient, connected_orient)
                    col_not = random.sample(col_not_r, min(1,len(col_not_r)))
                    noncol_not = random.sample(noncol_not_r,min(1,len(noncol_not_r)))
                    col_noncol_not = random.sample(col_noncol_not_r,min(1,len(col_noncol_not_r)))
                    new_edges, edges,g = NewEdge_IntProg(noVer,col_not,noncol_not,col_noncol_not,edges,col_orient,noncol_orient,connected_orient,noVer)
                
                new_edges.extend(new_edges_i)
                edges.extend(edges_i)
                
                
                for t_e in [[0,-1,1],[0,-2,1],[0,-3,1],[0,-1,3],[0,-2,3],[0,-3,3]]:
                    if t_e not in edges:
                        new_edges.append(t_e)
                        edges.append(t_e)
                
                
            
                unused_edges = []
                for i in range(noVer):    
                    for j in range(i+1,noVer):  
                            for edge_dir in [-1, -2, -3]:
                                unused_edges.append([i, edge_dir, j]) 
                               
                for this_new_edge in edges:                  
                    unused_edges.remove(this_new_edge)  
                
        D_est_int_all = np.zeros((noVer,noVer),dtype=int)
        E_est_int_all = np.zeros((noVer,noVer),dtype=int)
        
        for i in range(noVer):
            for j in range(i, noVer):
                if ordered([i,-3,j]) in edges:
                    E_est_int_all[i,j] = -1
                    E_est_int_all[j,i] = -1
                if ordered([i,-1,j]) in edges and ordered([i,-2,j]) in edges:
                    D_est_int_all[i,j] = -3
                    D_est_int_all[j,i] = -3
                    
                elif ordered([i,-1,j]) in edges:
                    D_est_int_all[i,j] = -1
                    D_est_int_all[j,i] = -2
                elif ordered([i,-2,j]) in edges:
                    D_est_int_all[i,j] = -2
                    D_est_int_all[j,i] = -1
                    
        dum_verts_int_all = []
        for ii in vertices:
            add_verts = []
            for jj in vertices:
                if D_est_int_all[ii,jj]!=0 or E_est_int_all[ii,jj]!=0:
                    add_verts.append(jj)
            dum_verts_int_all.append(add_verts)
                            
            
        
        
        path_con_lim,path_edge_lim,path_length_lim,path_IV_violater = con_edge_disc_lim(D_est_int_all,E_est_int_all, dum_verts_int_all, noVer,maxlength)    
        
        obj_val,runTime, C_not_yet_satisfied,C_not_yet_satisfied_ind,S_not_yet_satisfied,S_not_yet_satisfied_ind,D_est_int,E_est_int,dum_verts_int,edges_used_index,store_index,mod_status = MainintProg_searchmatrix(S, C,w_s,w_c, noVer,path_con_lim,path_edge_lim,path_length_lim,edges, edges_used_index,1,previous_graph_edge_indices,path_IV_violater,validIV,it_no)  

        
        
        D_IP_ASP = np.zeros((noVer,noVer),dtype=int)
        E_IP_ASP = -E_est_int
       
        for ii in vertices:
           for ii_2 in vertices:
               if D_est_int[ii,ii_2]==-2 or D_est_int[ii,ii_2]==-3:
                   D_IP_ASP[ii,ii_2] = 1
        
        
        S_violated_o, C_not_yet_satisfied_o = graph_postprocess(S, C, C_not_yet_satisfied, D_est_int,E_est_int, dum_verts_int, noVer)  
      
        
        errors = 0
        
        this_error_weigths_S = []
        this_error_weigths_C = []
        
        
        for this_kk in S_violated_o.keys():
            
            S_violated_o[this_kk] = [list(x) for x in set(tuple(x) for x in S_violated_o[this_kk])]
            unique_data = [list(x) for x in set(tuple(x) for x in S_violated_o[this_kk])]
            S_violated_ind = [S[this_kk].index(t_s_v) for t_s_v in unique_data]
            error_weights = [w_s[this_kk][this_kk_ind] for this_kk_ind in S_violated_ind]
            this_error_weigths_S.extend(error_weights)
            errors = errors + sum(error_weights)

            
        for this_kk in C_not_yet_satisfied_o.keys():

            C_not_yet_satisfied_o[this_kk] = [list(x) for x in set(tuple(x) for x in C_not_yet_satisfied_o[this_kk])]
            unique_data = [list(x) for x in set(tuple(x) for x in C_not_yet_satisfied_o[this_kk])]
            C_not_yet_satisfied_ind = [C[this_kk].index(t_s_v) for t_s_v in unique_data]
            error_weights = [w_c[this_kk][this_kk_ind] for this_kk_ind in C_not_yet_satisfied_ind]
            this_error_weigths_C.extend(error_weights)
            errors = errors + sum(error_weights)

        

        num_ip = num_ip+1
        
        
        S_violated_all[num_ip] = S_violated_o
        C_not_yet_satisfied_all[num_ip] = C_not_yet_satisfied_o
            
        error_weights_violated.append(this_error_weigths_S+this_error_weigths_C)
        
        S_all_weigths = [a_weight_this for a_weight in w_s.values() for a_weight_this in a_weight]
        C_all_weigths = [a_weight_this for a_weight in w_c.values() for a_weight_this in a_weight]
        
        
        S_all_weigths = set(S_all_weigths).difference(set(this_error_weigths_S))
        C_all_weigths = set(C_all_weigths).difference(set(this_error_weigths_C))   
        
        satisfied_weigths = list(S_all_weigths) + list(C_all_weigths)      
        all_satisfied_weigths.append(satisfied_weigths)
        
        all_errors.append(errors)  
               
       
        previous_graph_edge_indices.append(store_index)
            
            
        toc_alg = timeit.default_timer() 
        tot_time = toc_alg - tic_alg
        
        while tot_time<500 and now_return: 
            
            it_no = it_no +1
            obj_val,runTime, C_not_yet_satisfied,C_not_yet_satisfied_ind,S_not_yet_satisfied,S_not_yet_satisfied_ind,D_est_int,E_est_int,dum_verts_int,edges_used_index,store_index,mod_status = MainintProg_searchmatrix(S, C, w_s,w_c, noVer,path_con_lim,path_edge_lim,path_length_lim,edges, edges_used_index,1,previous_graph_edge_indices,path_IV_violater,validIV,it_no)  
            
            
            if previous_graph_edge_indices==[]:
                break
            
            if mod_status == 3:
                pdb.set_trace()
                
                return(S_violated_all,C_not_yet_satisfied_all,tot_time,all_errors,previous_graph_edge_indices,error_weights_violated,all_satisfied_weigths)
            
            
            D_IP_ASP = np.zeros((noVer,noVer),dtype=int)
            E_IP_ASP = -E_est_int
           
            for ii in vertices:
               for ii_2 in vertices:
                   if D_est_int[ii,ii_2]==-2 or D_est_int[ii,ii_2]==-3:
                       D_IP_ASP[ii,ii_2] = 1
           
            
            
            
            S_violated_o, C_not_yet_satisfied_o = graph_postprocess(S, C, C_not_yet_satisfied, D_est_int,E_est_int, dum_verts_int, noVer)  
            
            errors = 0
            this_error_weigths_S = []
            this_error_weigths_C = []
            
         
            for this_kk in S_violated_o.keys():
                
                S_violated_o[this_kk] = [list(x) for x in set(tuple(x) for x in S_violated_o[this_kk])]
                unique_data = [list(x) for x in set(tuple(x) for x in S_violated_o[this_kk])]
                S_violated_ind = [S[this_kk].index(t_s_v) for t_s_v in unique_data]
                error_weights = [w_s[this_kk][this_kk_ind] for this_kk_ind in S_violated_ind]
                this_error_weigths_S.extend(error_weights)
                errors = errors + sum(error_weights)

                
            for this_kk in C_not_yet_satisfied_o.keys():

                C_not_yet_satisfied_o[this_kk] = [list(x) for x in set(tuple(x) for x in C_not_yet_satisfied_o[this_kk])]
                unique_data = [list(x) for x in set(tuple(x) for x in C_not_yet_satisfied_o[this_kk])]
                C_not_yet_satisfied_ind = [C[this_kk].index(t_s_v) for t_s_v in unique_data]
                error_weights = [w_c[this_kk][this_kk_ind] for this_kk_ind in C_not_yet_satisfied_ind]
                this_error_weigths_C.extend(error_weights)
                errors = errors + sum(error_weights)

            
            num_ip = num_ip+1                        
            S_violated_all[num_ip] = S_violated_o
            C_not_yet_satisfied_all[num_ip] = C_not_yet_satisfied_o
    
            error_weights_violated.append(this_error_weigths_S+this_error_weigths_C)
            
            S_all_weigths = [a_weight_this for a_weight in w_s.values() for a_weight_this in a_weight]
            C_all_weigths = [a_weight_this for a_weight in w_c.values() for a_weight_this in a_weight]
            
            
            S_all_weigths = set(S_all_weigths).difference(set(this_error_weigths_S))
            C_all_weigths = set(C_all_weigths).difference(set(this_error_weigths_C))   
            
            satisfied_weigths = list(S_all_weigths) + list(C_all_weigths)      
            all_satisfied_weigths.append(satisfied_weigths)  
                
                   
            all_errors.append(errors)    
           
            previous_graph_edge_indices.append(store_index)
                              
            toc_alg = timeit.default_timer() 
            tot_time = toc_alg - tic_alg

            print(tot_time)
            
            
       
    
    toc_alg = timeit.default_timer() 
    tot_time = toc_alg - tic_alg
    

    
    
    return(S_violated_all,C_not_yet_satisfied_all,tot_time,all_errors,previous_graph_edge_indices,error_weights_violated,all_satisfied_weigths)
    
 
        
        
        
        
        
        
        



