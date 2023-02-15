
"""
EdgeGen

"""




import sys
import numpy as np
import pandas as pd 
import random
import timeit
from Edge_IntProg import NewEdge_IntProg
from Triples_connected_in_both import generate_triples
from Triple_orient import update_triple_orientation
from Update_triples import update_triples
from Update_triples_random import update_triples_random
from edge_connected_info_limLength import con_edge_disc_lim
from Search_IntProg_matrix  import MainintProg_searchmatrix
from f_graphPostprocess import graph_postprocess
split_dic = lambda txt_ii : [ int(txii) for txii in txt_ii.split('_') ] 
import pdb

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

def EdgeGen(noVer,S,C):

      
    maxlength = 3
    previous_graph_edge_indices = []              
                     
    unused_edges = []
    for i in range(noVer):    
        for j in range(i+1,noVer):  
            if '%s_%s'%(i,j) not in S.keys():
                for edge_dir in [-1, -2, -3]:
                    unused_edges.append([i, edge_dir, j])  
    
    

   
    collider_triple_initial,noncollider_triple_initial, col_noncol_triple_initial,edges,no_edge,col_orient,noncol_orient,connected_orient,connected_pairs = generate_triples(noVer, S, C)
    
    tic_alg =   timeit.default_timer()              
    new_edges, edges,g = NewEdge_IntProg(noVer,collider_triple_initial,noncollider_triple_initial,col_noncol_triple_initial,edges,col_orient,noncol_orient,connected_orient,noVer)
    initial_edges = edges.copy()
            
    for this_new_edge in new_edges:                  
        unused_edges.remove(this_new_edge)      
                                
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
    
    path_con_lim,path_edge_lim,path_length_lim = con_edge_disc_lim(D_est,E_est, dum_verts, noVer,maxlength) 
   
    obj_val, runTime, C_not_yet_satisfied, C_not_yet_satisfied_ind, S_not_yet_satisfied, S_not_yet_satisfied_ind, D_est_int, E_est_int, dum_verts_int, edges_used_index, store_index = MainintProg_searchmatrix(S, C, noVer, path_con_lim, path_edge_lim, path_length_lim, edges, [], 0, previous_graph_edge_indices)  
    obj_val_old = obj_val
        
    
    S_violated_o, C_not_yet_satisfied_o = graph_postprocess(S, C, C_not_yet_satisfied, D_est_int,E_est_int, dum_verts_int, noVer)  
    
     
    previous_graph_edge_indices.append(store_index)
        
    
  
    it_no = 0   
    
    while any(np.array(list(map(len,C_not_yet_satisfied_o.values()))) > 0) or any(np.array(list(map(len,S_violated_o.values()))) > 0):
        
        it_no = it_no +1                 
                       
        col_orient, noncol_orient, connected_orient = update_triple_orientation(collider_triple_initial, noncollider_triple_initial, col_noncol_triple_initial, col_orient, noncol_orient, connected_orient,edges)
        col_not, noncol_not,col_noncol_not = update_triples(C_not_yet_satisfied_o, collider_triple_initial, noncollider_triple_initial, col_noncol_triple_initial, col_orient, noncol_orient, connected_orient)
        
        if col_noncol_not!=[]:
            pdb.set_trace()
        
        if noncol_not!=[] or noncol_not!=[] or col_noncol_not!=[]:
            new_edges, edges,g = NewEdge_IntProg(noVer,col_not,noncol_not,col_noncol_not,edges,col_orient,noncol_orient,connected_orient,noVer)
       
        else:
            
            # print("**********************************************************")
            # print("RANDOM EDGE")
            # print("**********************************************************")
            
            col_not_r, noncol_not_r,col_noncol_not_r = update_triples_random(C_not_yet_satisfied_o, collider_triple_initial, noncollider_triple_initial, col_noncol_triple_initial, col_orient, noncol_orient, connected_orient)
            col_not = random.sample(col_not_r, min(1,len(col_not_r)))
            noncol_not = random.sample(noncol_not_r,min(1,len(noncol_not_r)))
            col_noncol_not = random.sample(col_noncol_not_r,min(1,len(col_noncol_not_r)))
            new_edges, edges,g = NewEdge_IntProg(noVer,col_not,noncol_not,col_noncol_not,edges,col_orient,noncol_orient,connected_orient,noVer)

            
                            
        for this_new_edge in new_edges:                  
            unused_edges.remove(this_new_edge)  
            
        if new_edges == []:
            # print("**********************************************************")
            # print("LENGTH INCREASED")
            # print("**********************************************************")
          
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
                # print("**********************************************************")
                # print("RANDOM EDGE")
                # print("**********************************************************")
                
                col_not_r, noncol_not_r,col_noncol_not_r = update_triples_random(C_not_yet_satisfied_o, collider_triple_initial, noncollider_triple_initial, col_noncol_triple_initial, col_orient, noncol_orient, connected_orient)
                col_not = random.sample(col_not_r, min(1,len(col_not_r)))
                noncol_not = random.sample(noncol_not_r,min(1,len(noncol_not_r)))
                col_noncol_not = random.sample(col_noncol_not_r,min(1,len(col_noncol_not_r)))
                new_edges, edges,g = NewEdge_IntProg(noVer,col_not,noncol_not,col_noncol_not,edges,col_orient,noncol_orient,connected_orient,noVer)

            unused_edges = []
            for i in range(noVer):    
                for j in range(i+1,noVer):  
                    if '%s_%s'%(i,j) not in S.keys():
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
                            
            
       
                    
        path_con_lim,path_edge_lim,path_length_lim = con_edge_disc_lim(D_est_int_all,E_est_int_all, dum_verts_int_all, noVer,maxlength)    
        
        obj_val,runTime, C_not_yet_satisfied,C_not_yet_satisfied_ind,S_not_yet_satisfied,S_not_yet_satisfied_ind,D_est_int,E_est_int,dum_verts_int,edges_used_index,store_index = MainintProg_searchmatrix(S, C, noVer,path_con_lim,path_edge_lim,path_length_lim,edges, edges_used_index,1,previous_graph_edge_indices)  
            
     
        S_violated_o, C_not_yet_satisfied_o = graph_postprocess(S, C, C_not_yet_satisfied, D_est_int,E_est_int, dum_verts_int, noVer)  
        
       
        previous_graph_edge_indices.append(store_index)
            
            
        toc_alg = timeit.default_timer() 
        tot_time = toc_alg - tic_alg
        # if tot_time>2500:
        #     break
        
 
        
    toc_alg = timeit.default_timer() 
    tot_time = toc_alg - tic_alg
    
    
    return(tot_time)
    
 
        
        
        
        
        
        
        



