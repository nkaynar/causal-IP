
"""
Algorithm 2: G-Postprocess sub-algorithm part 2
"""
import gc
from itertools import combinations 
import pdb
import numpy as np
import timeit
import sys
from numpy.linalg import multi_dot
import itertools

split_dic = lambda txt_ii : [ int(txii) for txii in txt_ii.split('_') ] 


def find_colliders(dir_list):    
    colliders = []
    for ii in range(int((len(dir_list)-1)/2)-1):
        if (dir_list[2*ii+1] in [-1, -3]) and (dir_list[2*ii+3] in [-2,-3]):
            colliders.append(dir_list[2*ii+2])
    return(colliders)
    
def find_noncolliders(dir_list):    
    noncolliders = []
    for ii in range(int((len(dir_list)-1)/2)-1):
        if (dir_list[2*ii+1] in [-1, -3] and dir_list[2*ii+3] in [-2,-3]):
            noncolliders.append(dir_list[2*ii+2])
    return(noncolliders)

def if_dir_paths(dir_list):    
    directed_path = 0
    edge_directions = dir_list[1::2] 
    if all(c == -1 for c in edge_directions):
        directed_path = 1 #i----> j
    elif all(c == -2 for c in edge_directions):
         directed_path = 2#i<---- j
    return(directed_path)

def which_edges(dir_list):
    edges_return = []
    for ii in range(int((len(dir_list)-1)/2)):
        edges_return.append(ordered(dir_list[2*ii:2*(ii+1)+1:1]))
    return(edges_return)  

def find_all_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if not start in graph:
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = find_all_paths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths

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
        if a[1]==-4:
            i_1 = a[2]
            i_2 = -3
            i_3 = a[0]
    else:
        i_1 = a[0]
        if a[1]==-4:
            i_2 = -3
        else:
            i_2 = a[1]
        i_3 = a[2]
        
    return([i_1,i_2,i_3])         
        


def find_descendants(D_true,noVer):
    child = [[] for ind in range(noVer)]
    D_true_child = D_true.copy()
    D_true_child[D_true_child==-2] = 0
    D_true_child[D_true_child==-3] = 1
    for i in range(noVer):
        add = [ind for ind in range(noVer) if D_true_child[i,ind]!=0 and ind!=i]
        child[i].extend(add)
        
    unique_child =  [[] for ind in range(noVer)] 
    D_true_multiplication = D_true_child.copy()
    for i in range(noVer):        
        D_true_multiplication = np.dot(D_true_multiplication, D_true_child)
        for ii in range(noVer):
            add = [ind for ind in range(noVer) if D_true_multiplication[ii,ind]!=0 and ind!=ii]
            child[ii].extend(add)
    for i in range(noVer):
        unique_child[i] = list(set(child[i]))
    return(unique_child)
        

                
def conedge_compute_pairs(var_list_in): 

    i, j, noVer, S_keys, S_ij, C_not_yet_satisfied_2_keys, C_not_yet_satisfied_2_ij, D_true, E_true, \
        vertices, graph, S_violated_ij, all_edges = var_list_in
        
        
    pair_ij = f'{i}_{j}'
                   
    # d-separation: 10 for d-separated, 1 for d-connected, 2 for not applicable
    path_con = {}
    path_edge = {}
    path_length = {}
   
    path_dir_index ={}
    path_dir_index[pair_ij] = []
    path_col_index = {}
    path_col_index[pair_ij] = []
    path_noncollider = {}
    path_noncollider[pair_ij] = []
    path_collider = {}
    path_collider[pair_ij] = []
    path_directed = {}
    path_directed[pair_ij] = []
    path_withcollider = {}
    path_withcollider[pair_ij] = []
    path_des_req = {}
    path_des_req[pair_ij] = []


    this_collider = []
    this_noncollider = []
    there_is_collider = []
    this_dirpath = []
    c_subsets={}
    
    for len_1 in range(len(vertices)-1):
        if pair_ij not in  c_subsets.keys():
            c_subsets[pair_ij] = list(combinations(set(vertices).difference(set([i,j])), len_1)) 
            
        else:
            c_subsets[pair_ij].extend(list(combinations(set(vertices).difference(set([i,j])), len_1)))
    c_subsets[pair_ij] = list(map(list, c_subsets[pair_ij]))
    
    
    critical_c = []
    if pair_ij in C_not_yet_satisfied_2_keys:
        critical_c = C_not_yet_satisfied_2_ij.copy()
        #critical_c_index = self.C_not_yet_satisfied_ind_2.copy()
        if pair_ij in S_keys:
            critical_c.extend(S_ij)
    else:
        if pair_ij in S_keys:
            critical_c = S_ij.copy()
     
    # --- find critical_c_index ---        
    critical_c_np = np.asarray(critical_c, dtype=object)

    if len(critical_c) == 1:
        critical_c_index = [ c_subsets[pair_ij].index(critical_c[0]) ]
    elif critical_c_np.ndim == 2:
        critical_c_index = [ c_subsets[pair_ij].index(c_np_ii) for c_np_ii in critical_c ]
    else:
        c_subsets_np = np.asarray(c_subsets[pair_ij], dtype=object)
        cs_sindex = np.argsort(c_subsets_np)
    
        sorted_cs_sindex = np.searchsorted(c_subsets_np[cs_sindex], critical_c_np)
        critical_c_index = np.take(cs_sindex, sorted_cs_sindex, mode='clip')
    # --- o ---
    
    
    # Find the paths btw comb_1
    # This will return undirected paths.
    paths = find_all_paths(graph, i, j)                  
    path_index = -1
    # Find all paths using the directions stored in D_true
    for pp in range(len(paths)): # This for loop is over all the paths bwt comb_1
        d_paths = []
        edge_info = []
        con_info = []
        path_tuple = [[paths[pp][ii], paths[pp][ii+1]] for ii in range(len(paths[pp]) - 1)] # Find all the 
                                                                                             # consecutive nodes in a path
        for tt in path_tuple:            
            ind1 = tt[0]
            ind2 = tt[1]   
            edge_info.append(D_true[ind1][ind2])
            con_info.append(E_true[ind1][ind2])
         # Store the direction of edges as an array in edge_info_matrix
        edge_info_matrix = np.array(edge_info) 
         
         
        if -3 in edge_info_matrix: 
            # If both i --> j and i<-- j present, we need to separates the paths that uses different edges.
                                    ## To do so replace -3 with -1 and -2.
            for this_col in np.where(np.array(edge_info) ==-3)[0]: 
                edge_info_matrix = np.vstack([edge_info_matrix, edge_info_matrix])            
                edge_info_matrix[0:int(edge_info_matrix.shape[0]/2),this_col]=np.ones((int(edge_info_matrix.shape[0]/2)),)*-1
                edge_info_matrix[int(edge_info_matrix.shape[0]/2):int(edge_info_matrix.shape[0]),this_col]=np.ones((int(edge_info_matrix.shape[0]/2)),)*-2
         
         
            
        if len(edge_info_matrix.shape)>1: # If -3 is present
            paths_extended = np.array([paths[pp],]*edge_info_matrix.shape[0])
         
            for ii_ext in range(len(edge_info)):  # Number of columns
                col_no= ii_ext*2+1 
                # Insert the direction info between nodes.
                paths_extended = np.insert(paths_extended, [col_no], edge_info_matrix[:,ii_ext].reshape(-1,1), axis=1)
                # Even numbered indices in paths_extended corresponds to nodes and odd numbered indices are for edge information.
             
             
        elif len(edge_info_matrix.shape)==1: # If -3 is not present
            paths_extended = paths[pp]
            for ii_ext in range(len(edge_info)):  # Number of columns
                col_no= ii_ext*2+1
                paths_extended = np.insert(paths_extended, [col_no], edge_info_matrix[ii_ext].reshape(-1,1))
         
        # tic_alg = timeit.default_timer()        
        if -1 in con_info:
            for this_con in np.where(np.array(con_info) ==-1)[0]: 
                if len(edge_info_matrix.shape)>1:
                    dummy_check = edge_info_matrix[0]
                else:
                    dummy_check = edge_info_matrix
                if not isinstance(dummy_check, np.ndarray):
                    dummy_check=[dummy_check]
                if not dummy_check[this_con] == 0:
                    paths_extended_con = paths_extended.copy()
                    
                    if len(paths_extended_con.shape)>1:
                        for this_ext_num in range(len(paths_extended_con)):
                            paths_extended_con[this_ext_num][2*this_con+1] = -4
                    else:
                        paths_extended_con[2*this_con+1] = -4 
                         
                    paths_extended = np.vstack([paths_extended, paths_extended_con]) 
                     
             
            for this_con in np.where(np.array(con_info) ==-1)[0]: 
                if len(edge_info_matrix.shape)>1:
                    dummy_check = edge_info_matrix[0]
                else:
                    dummy_check = edge_info_matrix
                if not isinstance(dummy_check, np.ndarray):
                    dummy_check=[dummy_check]
                 
                if dummy_check[this_con] == 0:
                    if len(paths_extended.shape)==1:
                        paths_extended[2*this_con+1] = -4*np.ones((1,1), dtype=np.uint8)
                    else:
                        paths_extended[:,2*this_con+1] = -4*(np.ones((1,len(paths_extended[:,this_con])), dtype=np.uint8)[0])
                     
     
                 
        # Append the paths individually to d_paths that stores the paths between pairs with direction info
        # tic_alg = timeit.default_timer() 
        if paths_extended.ndim>1:
            for add in range(paths_extended.shape[0]):
                if not any(list(paths_extended[add])==list(d_paths[ii_dp]) for ii_dp in range(len(d_paths))):
                    d_paths.append(paths_extended[add].tolist())
        else:
            d_paths.append(paths_extended.tolist()) 
        # toc_alg = timeit.default_timer() 
             
    
    # paths_dict['%s_%s'%(comb_1[0],comb_1[1])] = d_paths
         #this_path.append(d_paths)
                       
         
        for d_p in range(len( d_paths)):
            path_index = path_index+1
            current_path = d_paths[d_p]
            collider= []
            noncollider = []
            if len(current_path)>3:
                this_num_edges = int((len(current_path)-1)/2)
                for ii in range(this_num_edges-1):
                    if current_path[2*ii+1] in [-1,-4] and current_path[2*(ii+1)+1] in [-2,-4]:
                        collider.append(current_path[2*(ii+1)])
                    else:
                        noncollider.append(current_path[2*(ii+1)])
       
            this_collider.append(collider)
            this_noncollider.append(noncollider)
            if len(collider)>0:
                there_is_collider.append(1)
            else:
                there_is_collider.append(0)
                 
            if if_dir_paths(current_path)==1:
                this_dirpath.append(1)
            elif if_dir_paths(current_path)==2:
                this_dirpath.append(2)
            else:
                this_dirpath.append(0)
                 
         
            c_des_req = []    
            violating_independence = 0
            dsep_info = np.zeros((2**(noVer-2)), dtype=np.uint8)
             
            
                     
            if len(critical_c)==0:
     
                if pair_ij in path_des_req.keys():
                    #path_con[pair_ij].append(dsep_info)
                    path_des_req[pair_ij].append(c_des_req)
                else:
                    #path_con[pair_ij] = [dsep_info]
                    path_des_req[pair_ij] = [c_des_req]                       
                 
                path_collider[pair_ij] = this_collider 
                path_noncollider[pair_ij] = this_noncollider
             
                path_directed[pair_ij] = this_dirpath
                path_withcollider[pair_ij] = there_is_collider                                                               
                
                continue
             

            for c_c_no, c_set in enumerate(critical_c):
                c_no = critical_c_index[c_c_no]
  
                col_ind = collider
                noncol_ind = noncollider
                # If all colliders in a path are in c_set and if c_set doesn't include any of the noncolliders on p,
                # Then this pair is d-connected conditional on c_set
                if len(set(noncol_ind).intersection(set(c_set)))==0:
                     if len(set(col_ind).difference(set(c_set)))==0:
                         dsep_info[c_no] = 1                             
                         if list(c_set) in C_not_yet_satisfied_2_ij:
                            C_not_yet_satisfied_2_ij.remove(list(c_set))
                            
                         elif list(c_set) in S_ij:                             
                             S_violated_ij.append(list(c_set))     
                             violating_independence = 1
                                 
                                  
                     elif c_no!=0: 
                         c_des_req.append(c_no) 
             
            if pair_ij in path_des_req.keys():                
                path_des_req[pair_ij].append(c_des_req)
            else:
                path_des_req[pair_ij] = [c_des_req]
     
    
        path_collider[pair_ij] = this_collider 
        path_noncollider[pair_ij] = this_noncollider
     
        path_directed[pair_ij] = this_dirpath
        path_withcollider[pair_ij] = there_is_collider
        
    if pair_ij in path_directed.keys():    
        path_dir_index = {pair_ij : [t_ind for t_ind, t_el in enumerate (path_directed[pair_ij]) if t_el==1 ], 
                          '%s_%s'%(j,i) : [t_ind for t_ind, t_el in enumerate (path_directed[pair_ij]) if t_el==2 ] }
    else:
        path_dir_index = {}
        path_dir_index[pair_ij] = []
        
    if pair_ij in path_withcollider.keys():
        path_col_index = {pair_ij : [t_ind for t_ind, t_el in enumerate (path_withcollider[pair_ij]) if t_el==1 ] }
    else:
        path_col_index = {}
        path_col_index[pair_ij] = []
        
        
      
    C_return = {pair_ij :C_not_yet_satisfied_2_ij }
    S_violated_return = {pair_ij : S_violated_ij}


    return [path_dir_index,path_col_index,path_collider,path_noncollider,path_des_req, 
            S_violated_return, C_return]


                

#%%

                     
def conedge_des_compute_pairs(var_list_in):
        
    
    i,j, noVer, S_keys, S_ij, S_violated_ij, C_not_yet_satisfied_keys, C_not_yet_satisfied_ij, \
        D_true, vertices, path_col_index_ij, path_collider_ij, path_noncollider_ij, path_des_req_ij = var_list_in
        

    pair_ij = f'{i}_{j}'
    
    des_store = find_descendants(D_true, noVer)
    for ii in range(noVer):
        des_store[ii].append([])


    critical_c = []
    if pair_ij in C_not_yet_satisfied_keys:
        critical_c = C_not_yet_satisfied_ij.copy()
        if pair_ij in S_keys:
            critical_c.extend(S_ij)
    else:
        if pair_ij in S_keys:
            critical_c = S_ij.copy()
            
            
    if critical_c==[]:
        C_return = { pair_ij : C_not_yet_satisfied_ij } 
        S_violated_return= {pair_ij : S_violated_ij } 
        
        return [S_violated_return, C_return]


    c_subsets={}
    for len_1 in range(len(vertices)-1):
        if '%s_%s'%(i,j) not in  c_subsets.keys():
            c_subsets['%s_%s'%(i,j)] = list(combinations(set(vertices).difference(set([i,j])), len_1)) 
        else:
            c_subsets['%s_%s'%(i,j)].extend(list(combinations(set(vertices).difference(set([i,j])), len_1)))
   
    
    for i_n in path_col_index_ij:                       

        colliders = path_collider_ij[i_n]
        noncolliders = path_noncollider_ij[i_n] 
        this_des = []
        for ii in colliders:
            add_this = [ t_d for t_d in des_store[ii] if t_d not in noncolliders and t_d!=[]]
            add_this.append(ii)
            this_des.append(add_this)
            
        for c_no in path_des_req_ij[i_n]:
            
            c_set = c_subsets[pair_ij][c_no]
            
            if min([len(set(this_col_combo).intersection(set(c_set))) for this_col_combo in this_des])>0:
                
                if list(c_set) in C_not_yet_satisfied_ij:
                    C_not_yet_satisfied_ij.remove(list(c_set))
                   
                elif list(c_set) in S_ij and list(c_set) not in S_violated_ij:
                        S_violated_ij.append(list(c_set))
                    
    
    C_return = { pair_ij : C_not_yet_satisfied_ij } 
    S_violated_return= {pair_ij : S_violated_ij } 

    return [S_violated_return, C_return]


