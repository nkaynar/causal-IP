


"""
CAUSALIP
"""


from gurobipy import *
import pandas as pd
import pdb
import csv
from itertools import combinations 
import numpy as np
import sys,timeit
import scipy.sparse as sp
from scipy import sparse
from scipy.sparse import coo_matrix, vstack
from scipy.sparse import csr_matrix

import pickle
from sklearn.feature_extraction import DictVectorizer

split_dic = lambda txt_ii : [ int(txii) for txii in txt_ii.split('_') ] 

from tqdm import tqdm


from itertools import chain, combinations

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

#no inconsistency
#path based
# dsep_all_dict 0 if d-sep, 1 if d-con, 3 if not applicable

def MainintProg_searchmatrix(S, C, V, path_con, path_edge, path_length, edges_in, edges_used_index, prev_sol, previous_graph_edge_indices):
    print("girdi")
    #sys.exit()
    vertices = list(range(V))
    pairs = list(combinations(vertices, 2))
    num_path_dict = {}
    for this_key in list(path_con):       
        num_path_dict[this_key] = len(path_con[this_key]) 
    
    c_subsets={}
    S_index = {}
    C_index = {}
    for i in range(V):
         for j in range(i,V):
             if not i==j:
                 this_l = len(vertices)-1
             else:
                 this_l = len(vertices)
             for len_1 in range(this_l):
             #for len_1 in range(5):
                 if '%s_%s'%(i,j) not in  c_subsets.keys():
                     c_subsets['%s_%s'%(i,j)] = list(combinations(set(vertices).difference(set([i,j])), len_1)) 
                 else:
                     c_subsets['%s_%s'%(i,j)].extend(list(combinations(set(vertices).difference(set([i,j])), len_1)))
             
             c_subsets['%s_%s'%(i,j)] = list(map(list, c_subsets['%s_%s'%(i,j)]))

             if '%s_%s'%(i,j) in S.keys():
                 S_np = np.asarray(S['%s_%s'%(i,j)], dtype=object)
                 
                 if len(S['%s_%s'%(i,j)]) == 1:
                     S_index['%s_%s'%(i,j)] = [ c_subsets['%s_%s'%(i,j)].index(S['%s_%s'%(i,j)][0]) ]
                 elif S_np.ndim == 2:
                     S_index['%s_%s'%(i,j)] = [ c_subsets['%s_%s'%(i,j)].index(s_np_ii) for s_np_ii in S['%s_%s'%(i,j)] ]
                 else:
                     c_subsets_np = np.asarray(c_subsets['%s_%s'%(i,j)], dtype=object)
                     cs_sindex = np.argsort(c_subsets_np)
                     
                     sorted_S_sindex = np.searchsorted(c_subsets_np[cs_sindex], S_np)
                     S_index['%s_%s'%(i,j)] = np.take(cs_sindex, sorted_S_sindex, mode='clip')
             else:
                  S_index['%s_%s'%(i,j)] = []
                  
             if '%s_%s'%(i,j) in C.keys():
                 C_np = np.asarray(C['%s_%s'%(i,j)], dtype=object)
                 
                 if len(C['%s_%s'%(i,j)]) == 1:
                     C_index['%s_%s'%(i,j)] = [ c_subsets['%s_%s'%(i,j)].index(C['%s_%s'%(i,j)][0]) ]
                 elif C_np.ndim == 2:
                     C_index['%s_%s'%(i,j)] = [ c_subsets['%s_%s'%(i,j)].index(c_np_ii) for c_np_ii in C['%s_%s'%(i,j)] ]
                 else:
                     c_subsets_np = np.asarray(c_subsets['%s_%s'%(i,j)], dtype=object)
                     cs_sindex = np.argsort(c_subsets_np)
                     
                     sorted_C_sindex = np.searchsorted(c_subsets_np[cs_sindex], C_np)
                     C_index['%s_%s'%(i,j)] = np.take(cs_sindex, sorted_C_sindex, mode='clip')
             else:
                  C_index['%s_%s'%(i,j)] = []
                  
                  
                  
   
    all_edges = []
    for node1 in vertices:    
         for node2 in vertices:
             if node1<node2:
                 for edge_dir in [-1, -2, -3]:
                 #for edge_dir in [-1, -2]:
                     all_edges.append([node1, edge_dir, node2])  
    #aa = '123_2'.split('_')
    
    #Initialize model. 
    mod = Model()
    mod.Params.LogToConsole = 0
    mod.Params.OutputFlag = 0
   # mod.setParam('TimeLimit', 600)
    
    vars_tup1 = [(e) for e in range(len(all_edges))]
    
    path_keys = list(sorted(num_path_dict.keys()))
    path_keys_list = []
    for this_key in path_keys:      
        add_p_key = split_dic(this_key)
        if add_p_key[0]!=add_p_key[1]:
            path_keys_list.append(add_p_key)
    path_keys_list = list(sorted(path_keys_list))   
    
    C_keys = list(sorted(C.keys()))
    C_keys_list = []
    for this_key in C_keys:
        #add_key = [int(this_key[0]), int(this_key[2])]
        add_key = split_dic(this_key)
        C_keys_list.append(add_key)
    C_keys_list = list(sorted(C_keys_list))
        
    
    S_keys = list(sorted(S.keys()))
    S_keys_list = []
    for this_key in S_keys:
        #add_key = [int(this_key[0]), int(this_key[2])]
        add_key = split_dic(this_key)
        S_keys_list.append(add_key)
        
    S_keys_list = list(sorted(S_keys_list))
        
    vars_tup2 = [(i,j,p) for [i,j] in path_keys_list for p in range(num_path_dict['%s_%s'%(i,j)])] 
    vars_tup3 = [(i,j,k) for [i,j] in C_keys_list  for k in range(len(C['%s_%s'%(i,j)])) ]
    vars_tup4 = [(i,j,k) for [i,j] in S_keys_list  for k in range(len(S['%s_%s'%(i,j)])) ]
    
 
    x = mod.addMVar(len(vars_tup1),vtype=GRB.BINARY,name="x") 
    y = mod.addMVar(len(vars_tup2),vtype=GRB.BINARY,name="y")
    z = mod.addMVar(len(vars_tup3),vtype=GRB.CONTINUOUS,name="z")
    z_s = mod.addMVar(len(vars_tup4),vtype=GRB.CONTINUOUS,name="z_s")
   
    



    
    mod.update() 
   
    if prev_sol == 1:
        x.Start = edges_used_index
       
        w = mod.addMVar(len(previous_graph_edge_indices),vtype=GRB.BINARY,name="w")
        
        A_ng = np.zeros((len(previous_graph_edge_indices),len(vars_tup1)), dtype = np.int8)
        A_w = np.zeros((len(previous_graph_edge_indices),len(previous_graph_edge_indices)), dtype = np.int8)
        A_w2 = np.zeros((len(previous_graph_edge_indices),), dtype = np.int8)
        for old_g in range(len(previous_graph_edge_indices)):
            this_old_edges = previous_graph_edge_indices[old_g]
            A_ng[old_g,this_old_edges] = -1
            
            unused_edge_ind = [ ii for ii in range(len(all_edges)) if ii not in this_old_edges]
            A_ng[old_g,unused_edge_ind] = 1
            
            A_w[old_g,old_g] = 1
            A_w2[old_g,] = len(this_old_edges)
            
        #pdb.set_trace()    
        mod.addConstr(-A_w2 + A_w @ w  <= A_ng @ x)
      
        mod.addConstr(w  == 1)
        
        
        mod.update() 
        
            

        
    
    
    
    tic1 = timeit.default_timer()
    A1 = np.zeros(len(vars_tup1),dtype=np.uint8)
    for e in vars_tup1:
        if not all_edges[e] in edges_in:
            A1[e] = 1

    toc1 = timeit.default_timer()

        
    A1 = sparse.csr_matrix(A1)         
    mod.addConstr(A1 @ x == 0)  
  
    A2_rows = []
    A5_rows = []
    A5_cols = []
    A5_vals = []
    A6_vals = []
    A6_cols = []
    A6_rows = []
    A3 = np.zeros((len(vars_tup2),len(vars_tup1)),dtype=np.uint8)
    A4 = np.zeros(len(vars_tup2),dtype=np.uint8)
    count = -1
    count_2 = 0
    for (i,j) in path_keys_list:
        for p in range(num_path_dict['%s_%s'%(i,j)]):
            count = count+1
            A2_rows.append(count)            
            A3[count] = path_edge['%s_%s'%(i,j)][p]
            A4[count] = path_length['%s_%s'%(i,j)][p][0]-1
            #tighther formulation
            edge_on_p = np.where(path_edge['%s_%s'%(i,j)][p] == 1)[0]
            A6_cols.extend(list(np.where(path_edge['%s_%s'%(i,j)][p] == 1)[0]))
            A5_cols.extend([count for t_count in range(sum(path_edge['%s_%s'%(i,j)][p]))])

    A2_vals = [1 for ii in range(count+1)]
    A2 = csr_matrix((np.array(A2_vals), (np.array(A2_rows), np.array(A2_rows))), shape=(count+1,count+1 ))#.toarray()  
    A5_vals = [1 for ii in range(len(A5_cols))]
    A5_rows = [ii for ii in range(len(A5_cols))]
    A6_vals = [1 for ii in range(len(A6_cols))]
    A6_rows = [ii for ii in range(len(A6_cols))]
    A5 = csr_matrix((np.array(A5_vals), (np.array(A5_rows), np.array(A5_cols))), shape=(len(A5_vals),count+1))#.toarray()  
    A6 = csr_matrix((np.array(A6_vals), (np.array(A6_rows), np.array(A6_cols))), shape=(len(A6_vals),len(vars_tup1)))
    
    mod.addConstr(A2 @ y - A3 @ x>= -A4.transpose())
    mod.addConstr(A5 @ y- A6 @ x<=0)
    
    

   
    A7_rows = []
    A7_cols = []
    count = -1
    tot_path_no = 0

    for (i,j) in pairs:
        if '%s_%s'%(i,j) in C.keys():
            this_key = '%s_%s'%(i,j)    
            if this_key in path_keys and len(path_con[this_key])>0:      
                con_info = np.vstack(path_con[this_key])            
                for count_C in range(len(C['%s_%s'%(i,j)])):
                    count = count+1               
                    #num_c = c_subsets['%s_%s'%(i,j)].index(tuple(c_ii))   
                    num_c = C_index['%s_%s'%(i,j)][count_C]
                    con_paths = con_info[:,num_c]
                    path_indices = np.where(con_paths == 1)[0]
                    if len(path_indices)>0:
                        A7_cols.extend(path_indices+tot_path_no)
                        A7_rows.extend([count for ii in range(len(path_indices))])
            else:                 
                    count = count+len(C['%s_%s'%(i,j)])
                    
        tot_path_no = tot_path_no +  num_path_dict['%s_%s'%(i,j)]
        toco2 = timeit.default_timer() 
            
            
    A7_vals = [1 for ii in range(len(A7_cols))]  
    A7 = csr_matrix((np.array(A7_vals), (np.array(A7_rows), np.array(A7_cols))), shape=(len(vars_tup3),len(vars_tup2) ))                                          
    mod.addConstr(A7 @ y>= 1 - z) 
    toc111 = timeit.default_timer()   



 
    
    ticbak2 = timeit.default_timer()    
    count = -1
    tot_path_no = 0
    A8_rows = []
    A8_columns = []
    A9_rows = []
    A9_columns = []
    tot_cons_num = 0
    for (i,j) in tqdm(pairs):
        this_key = '%s_%s'%(i,j)
        if [i,j] in S_keys_list:   
            if this_key in path_keys and len(path_con[this_key])>0:
                con_info = np.vstack(path_con[this_key])                   
                for count_S in range(len(S[this_key])):
                    count = count+1                                                                               
                    num_c = S_index[this_key][count_S]
                    #if i==1 and j==2 and num_c==186:
                     #   sys.exit()
                    con_paths = con_info[:,num_c]
                    path_indices = np.where(con_paths == 1)[0]
                    if len(path_indices)>0:
                    #A8
                        A8_columns.extend([count for ii in path_indices])
                        A8_rows.extend([ii for ii in range(tot_cons_num,tot_cons_num+len(path_indices))])
                        
                        #A9
                        A9_columns.extend([tot_path_no+ii for ii in path_indices])
                        A9_rows.extend([ii for ii in range(tot_cons_num,tot_cons_num+len(path_indices))])
                        tot_cons_num = tot_cons_num+len(path_indices)
            else:
                count = count+len(S[this_key])
            
        tot_path_no = tot_path_no +  num_path_dict[this_key]
        
        
    data_A8 = [1 for ii in range(len(A8_rows))]
    data_A9 = [1 for ii in range(len(A9_rows))]   
    if len(A8_rows)>0:
        A8 = csr_matrix((np.array(data_A8), (np.array(A8_rows), np.array(A8_columns))), shape=(tot_cons_num,len(vars_tup4) ))#.toarray()  
        A9 = csr_matrix((np.array(data_A9), (np.array(A9_rows), np.array(A9_columns))), shape=(tot_cons_num,len(vars_tup2) ))#.toarray()  
        mod.addConstr( A8 @ z_s>= A9 @ y)     
        #sys.exit()
                    
 

        
    A10 = np.ones(len(vars_tup3),dtype=int)  
    A11 = 1000000*np.ones(len(vars_tup4),dtype=int) 
    #mod.addConstr( A11 @ z_s == 0)  
    
    
    A12 = 0.001*np.ones(len(vars_tup1),dtype=int) 

    mod.setObjective(A10 @ z+ A11 @ z_s, GRB.MINIMIZE)
   
                               
    mod.update()
   # mod.write('causality_path.mps') 
    #mod.setParam('TimeLimit', 600)
    mod.optimize()
    

            
    #pdb.set_trace()        
    obj_return = mod.objVal
    toc1 = timeit.default_timer()
    store_index = []
    for i in vars_tup1:
        if x[i].x==1:
            store_index.append(i)
    edges_used_in_graph = []   
    edges_used_index = x.x    
    dum_verts = [[] for _ in range(V)]
    D_est = np.zeros((V,V),dtype=int)
    E_est = np.zeros((V,V),dtype=int)
    
    for e in range(len(all_edges)):
        if x[e].x==1:            
            this_edge_info = all_edges[e]        
            edges_used_in_graph.append((this_edge_info[0],this_edge_info[2],-this_edge_info[1]-1))
            if -this_edge_info[1]-1==0:
                edges_used_in_graph.append((this_edge_info[2],this_edge_info[0],1))
            elif -this_edge_info[1]-1==1:
                edges_used_in_graph.append((this_edge_info[2],this_edge_info[0],0))
            else:
                edges_used_in_graph.append((this_edge_info[2],this_edge_info[0],2))
                
            dum_verts[this_edge_info[0]].append(this_edge_info[2])
            dum_verts[this_edge_info[2]].append(this_edge_info[0])
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
    for ii in vertices:
        for ii_2 in vertices:
            if D_est[ii,ii_2]==-1:
                D_est[ii_2,ii]=-2
            if D_est[ii,ii_2]==-2:
                D_est[ii_2,ii]=-1
            if D_est[ii,ii_2]==-3:
                D_est[ii_2,ii]=-3
                
    for ii in vertices:
        for ii_2 in vertices:
            if E_est[ii,ii_2]==-1:
                E_est[ii_2,ii]=-1
    toc2 = timeit.default_timer()            

  
    C_not_yet_satisfied = {}
    C_not_yet_satisfied_ind = {}
    pairs_not_yet_satisfied = {}
    for i in range(len(vars_tup3)):
        if z[i].x==1: 
           this_key = '%s_%s'%(vars_tup3[i][0],vars_tup3[i][1])
           if this_key in C_not_yet_satisfied.keys():
               C_not_yet_satisfied[this_key].append(C[this_key][vars_tup3[i][2]] )
               C_not_yet_satisfied_ind[this_key].append(vars_tup3[i][2] )
           else:
               C_not_yet_satisfied[this_key]= [C[this_key][vars_tup3[i][2]]]
               C_not_yet_satisfied_ind[this_key] = [vars_tup3[i][2]]
               
    S_not_yet_satisfied = {}
    S_not_yet_satisfied_ind = {}
    pairs_not_yet_satisfied = []
    for i in range(len(vars_tup4)):
        if z_s[i].x==1: 
            this_key = '%s_%s'%(vars_tup4[i][0],vars_tup4[i][1])
            if this_key in S_not_yet_satisfied.keys():
                S_not_yet_satisfied[this_key].append(S[this_key][vars_tup4[i][2]] )
                S_not_yet_satisfied_ind[this_key].append(vars_tup4[i][2])
            else:
                S_not_yet_satisfied[this_key]= [S[this_key][vars_tup4[i][2]]]
                S_not_yet_satisfied_ind[this_key] = [vars_tup4[i][2]]
         

    
    return(obj_return, mod.RunTime, C_not_yet_satisfied, C_not_yet_satisfied_ind, S_not_yet_satisfied, S_not_yet_satisfied_ind, D_est, E_est, dum_verts, edges_used_index, store_index)

          
        
        
        
        
        
        