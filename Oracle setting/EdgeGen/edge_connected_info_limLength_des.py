
"""
Generate paths with descendancies

"""

from itertools import combinations 
import pdb
import numpy as np
import sys
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
        
            
                

def con_edge_disc_lim(D_true,E_true, dum_verts, noVer,maxLength):    
    vertices= list(range(noVer))
    
    for ii in vertices:
        for jj in vertices:
            if ii in dum_verts[jj]:
                dum_verts[ii].append(jj)
        dum_verts[ii] = list(set((dum_verts[ii]))) 
        
    
    graph = dict(zip(vertices,dum_verts))   
            
            
    c_subsets={}
    for i in range(noVer):
         for j in range(i,noVer):
             if not i==j:
                 this_l = len(vertices)-1
             else:
                 this_l = len(vertices)
             for len_1 in range(this_l):
                 if '%s_%s'%(i,j) not in  c_subsets.keys():
                     c_subsets['%s_%s'%(i,j)] = list(combinations(set(vertices).difference(set([i,j])), len_1)) 
                 else:
                     c_subsets['%s_%s'%(i,j)].extend(list(combinations(set(vertices).difference(set([i,j])), len_1)))
                     
    all_edges = []
    for node1 in vertices:    
         for node2 in vertices:
             if node1<node2:
                 for edge_dir in [-1, -2, -3]:
                     all_edges.append([node1, edge_dir, node2])  
                     
        
    # Find all pairs of nodes
    pairs = list(combinations(vertices, 2))
    
    # d-separation: 10 for d-separated, 1 for d-connected, 2 for not applicable
    path_con = {}
    path_edge = {}
    path_length = {}
    path_noncollider = {}
    path_collider = {}
    path_directed = {}
    path_withcollider = {}
    path_des_req = {}
   
    for pair_no, comb_1 in enumerate(pairs): #pair_no give the index of the current pair, which is comb_1
    
        this_collider = []
        this_noncollider = []
        there_is_collider = []
        this_dirpath = []
        this_path = []
        i = comb_1[0]
        j = comb_1[1]
       
       
        # Find the paths btw comb_1
        # This will return undirected paths.
        paths = find_all_paths(graph,comb_1[0],comb_1[1])                  
        path_index = -1
        # Find all paths using the directions stored in D_true
        for pp in range(len(paths)): # This for loop is over all the paths bwt comb_1
            if len(paths[pp])>maxLength:
                #pdb.set_trace()
                continue
                       
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
                       
            if -3 in edge_info_matrix: # If both i --> j and i<-- j present, we need to separate the paths that use different edges.
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
                            paths_extended[2*this_con+1] = -4*np.ones((1,1), dtype=int)
                        else:
                            paths_extended[:,2*this_con+1] = -4*(np.ones((1,len(paths_extended[:,this_con])), dtype=int)[0])
           
                    
            # Append the paths individually to d_paths that stores the paths between pairs with direction info
            if paths_extended.ndim>1:
                for add in range(paths_extended.shape[0]):
                    if not any(list(paths_extended[add])==list(d_paths[ii_dp]) for ii_dp in range(len(d_paths))):
                        d_paths.append(paths_extended[add].tolist())
            else:
                d_paths.append(paths_extended.tolist())                
       # paths_dict['%s_%s'%(comb_1[0],comb_1[1])] = d_paths
            this_path.append(d_paths)

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
                    
            
                #find the edge indices
                edges_in_path_ind = []
                for e_n in range(int((len(current_path)-1)/2)):
                    this_edge = ordered(current_path[e_n*2:e_n*2+3])
                    
                    this_ind = all_edges.index(this_edge)
                    edges_in_path_ind.append(this_ind)
                dsep_info = np.zeros((len(c_subsets['%s_%s'%(i,j)])),dtype=int)
                
                edge_info = np.zeros((len(all_edges)),dtype=int) 
                for e_ind in edges_in_path_ind:
                    edge_info[e_ind] = 1
                    
                if '%s_%s'%(i,j) in path_edge.keys():
                    path_edge['%s_%s'%(i,j)].append(edge_info)
                else:
                    path_edge['%s_%s'%(i,j)] = [edge_info]
                    
                if '%s_%s'%(i,j) in path_length.keys():
                    path_length['%s_%s'%(i,j)].append([len(edges_in_path_ind)])
                else:
                    path_length['%s_%s'%(i,j)] = [[len(edges_in_path_ind)]]
                    
                #check if there is a d-connected path btw current pair   
                c_des_req = []    
                for c_no, c_set in enumerate(c_subsets['%s_%s'%(i,j)]):
              # Conditioning set doesn't include any of the nodes in current pair. 
                        # Check if there is a d-connected path without considering the descendats yet
                        
                       # for path_no in range(len(paths_dict['%s_%s'%(comb_1[0],comb_1[1])])): #for each path
                        col_ind = collider
                        noncol_ind = noncollider
                        # If all colliders in a path are in c_set and if c_set doesn't include any of the noncolliders on p,
                        # Then this pair is d-connected conditional on c_set
                        if len(set(noncol_ind).intersection(set(c_set)))==0:
                            if len(set(col_ind).difference(set(c_set)))==0:
                                dsep_info[c_no] = 1 
                            elif c_no!=0: 
                                c_des_req.append(c_no) 
               
                if '%s_%s'%(i,j) in path_con.keys():
                    path_con['%s_%s'%(i,j)].append(dsep_info)
                    path_des_req['%s_%s'%(i,j)].append(c_des_req)
                else:
                    path_con['%s_%s'%(i,j)] = [dsep_info]
                    path_des_req['%s_%s'%(i,j)] = [c_des_req]
    
        path_collider['%s_%s'%(i,j)] = this_collider 
        path_noncollider['%s_%s'%(i,j)] = this_noncollider
        path_directed['%s_%s'%(i,j)] = this_dirpath
        path_withcollider['%s_%s'%(i,j)] = there_is_collider
        
             
    path_dir_index ={}
    for i in range(noVer):
        for j in range(noVer):
            if i<j:
                path_dir_index['%s_%s'%(i,j)] = [t_ind for t_ind, t_el in enumerate (path_directed['%s_%s'%(i,j)]) if t_el==1 ]

            elif i>j:
                path_dir_index['%s_%s'%(i,j)] = [t_ind for t_ind, t_el in enumerate (path_directed['%s_%s'%tuple(sorted([i,j]))]) if t_el==2 ]
                
    path_col_index = {}
    for i in range(noVer):
        for j in range(i+1,noVer):
            path_col_index['%s_%s'%(i,j)] = [t_ind for t_ind, t_el in enumerate (path_withcollider['%s_%s'%(i,j)]) if t_el==1 ]



    des_store = find_descendants(D_true,noVer)
    for ii in range(noVer):
        des_store[ii].append([])
      


    for pair_no, comb_1 in enumerate(pairs):      
        i = comb_1[0]
        j = comb_1[1] 
        #pdb.set_trace()
        if '%s_%s'%(i,j) not in path_des_req.keys():
            continue
   
        if len(max(path_des_req['%s_%s'%(i,j)])) == 0:
            continue
                
        
        for i_n in path_col_index['%s_%s'%(i,j)]:   
                    
            dsep_info = np.zeros((len(c_subsets['%s_%s'%(i,j)])),dtype=int)
            colliders = path_collider['%s_%s'%(i,j)][i_n]
            noncolliders = path_noncollider['%s_%s'%(i,j)][i_n] 
            this_des = tuple([des_store[ii] for ii in colliders if ii not in noncolliders])
            paths_cover = []
            
            for i_num, i_c in enumerate(colliders):
                paths_cover_this = []
                for i_d in this_des[i_num]:
                    if i_d!=[] and i_d!=i and i_d!=j:
                      for i_p in path_dir_index['%s_%s'%(i_c,i_d)]:
                        paths_cover_this.append([i_c,i_d,i_p])
                    elif i_d==[]:
                        paths_cover_this.append([])
                paths_cover.append(paths_cover_this)
                
            this_path_cover_combo = []
            if len(paths_cover) == 1: 
                this_path_cover_combo = [[j_p] for j_p in paths_cover[0]]
            elif len(paths_cover) >= 1: 
                for i_c in itertools.product(*paths_cover):
                    this_path_cover_combo.append(i_c)
            del this_path_cover_combo[-1]
            
            for i_p in range(len(this_path_cover_combo)):
                edge_info = path_edge['%s_%s'%(i,j)][i_n].copy()
                con_info = path_con['%s_%s'%(i,j)][i_n].copy()
                col_subsets = set()
                t_comb = this_path_cover_combo[i_p]
                for this_ind_j, this_j in enumerate(t_comb):
                  if this_j!=[]:
                    col_subsets.add((this_j[0],this_j[1]))
                    new_edge_info = path_edge['%s_%s'%tuple(sorted([this_j[0],this_j[1]]))][this_j[2]]
                    edge_info = np.maximum(edge_info, new_edge_info)
                  else:
                      col_subsets.add(tuple([colliders[this_ind_j]]))
                     
                     
                for c_no in path_des_req['%s_%s'%(i,j)][i_n]:
                    c_set = c_subsets['%s_%s'%(i,j)][c_no]                    
                    if all(bool(set(this_ss) & set(c_set)) for this_ss in col_subsets ):
                        con_info[c_no] = 1
                                  
                path_con['%s_%s'%(i,j)].append(con_info)
                path_edge['%s_%s'%(i,j)].append(edge_info)
                path_length['%s_%s'%(i,j)].append([sum(edge_info)])
               
                   
                         

                    
    for this_key in c_subsets.keys():
        if this_key not in path_con.keys():
            path_con[this_key] = []
            path_edge[this_key] = []
            path_length[this_key] = []
            
            
    return(path_con,path_edge, path_length) 
         
