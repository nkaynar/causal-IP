


"""
NEWEDGESIP


"""



from gurobipy import *
import pdb
from itertools import combinations 
import numpy as np
import sys,timeit



split_dic = lambda txt_ii : [ int(txii) for txii in txt_ii.split('_') ] 


from itertools import chain, combinations

def ordered(a):
    
    if a[1]<a[0]:
        if a[2]==1:
            i_1 = a[1]
            i_2 = a[0]
            i_3 = 2
        if a[2]==2:
            i_1 = a[1]
            i_2 = a[0]
            i_3 = 1
        if a[2]==3:
            i_1 = a[1]
            i_2 = a[0]
            i_3 = 3
    else:
        i_1 = a[0]
        i_2 = a[1]
        i_3 = a[2]
        
    return(i_1,i_2,i_3)         

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def NewEdge_IntProg(V,collider_triple,noncollider_triple, col_noncol_triple, edges,col_orient,noncol_orient,connected_orient,noVer):


    # -->:1 <--:2, <-->:3
    all_edges = []
    g = []
    for i in range(noVer):
        for j in range(i+1,noVer):
            for edge_dir in [1, 2, 3]:
                all_edges.append((i, j, edge_dir)) 
                if [i, -edge_dir, j] in edges:
                    g.append(1)
                else:
                    g.append(0) 
                         
  #  if max(g)>0:
   #     pdb.set_trace()
    mod = Model()
    mod.Params.OutputFlag = 1
    vars_tup1 = [(i,j,k) for [i,j,k] in all_edges]
    x = mod.addVars(vars_tup1, vtype=GRB.BINARY, name="x")
    
    for (i,j,k) in collider_triple:
        g_c1_ind = all_edges.index(ordered([i,j,1]))
        g_c2_ind = all_edges.index(ordered([i,j,3]))
        mod.addConstr(x[ordered([i,j,1])]+g[g_c1_ind]+x[ordered([i,j,3])]+ g[g_c2_ind]>=1)
        
        g_c3_ind = all_edges.index(ordered([j,k,2]))
        g_c4_ind = all_edges.index(ordered([j,k,3]))
        mod.addConstr(x[ordered([j,k,2])]+g[g_c3_ind]+x[ordered([j,k,3])]+ g[g_c4_ind]>=1)
        
        
        if len(col_orient['%s_%s_%s'%(i,j,k)])>0:
            mod.addConstr(x[ordered([i,j,1])]+x[ordered([i,j,3])]+x[ordered([j,k,2])]+x[ordered([j,k,3])]>=1)
        
    for (i,j,k) in noncollider_triple:
        g_n1_ind = all_edges.index(ordered([i,j,1]))
        g_n2_ind = all_edges.index(ordered([i,j,2]))
        g_n3_ind = all_edges.index(ordered([i,j,3]))
        mod.addConstr(sum(x[ordered([i,j,t])] for t in range(1,4))+g[g_n1_ind]+g[g_n2_ind]+g[g_n3_ind]>=1)
        
        
        g_n4_ind = all_edges.index(ordered([j,k,1]))
        g_n5_ind = all_edges.index(ordered([j,k,2]))
        g_n6_ind = all_edges.index(ordered([j,k,3]))
        mod.addConstr(sum(x[ordered([j,k,t])] for t in range(1,4))+g[g_n4_ind]+g[g_n5_ind]+g[g_n6_ind]>=1)
        
        if len(noncol_orient['%s_%s_%s'%(i,j,k)])>0:
            mod.addConstr(sum(x[ordered([i,j,t])] for t in range(1,4))+sum(x[ordered([j,k,t])] for t in range(1,4))>=1)
        
        mod.addConstr(x[ordered([i,j,1])]<=g[g_n4_ind] +x[ordered([j,k,1])])
        mod.addConstr(x[ordered([i,j,3])]<=g[g_n4_ind] +x[ordered([j,k,1])])
        mod.addConstr(x[ordered([j,k,2])]<=g[g_n2_ind] +x[ordered([i,j,2])])
        mod.addConstr(x[ordered([j,k,3])]<=g[g_n2_ind] +x[ordered([i,j,2])])

        
     
        
    for (i,j,k) in col_noncol_triple:
        
        g_cn1_ind = all_edges.index(ordered([i,j,1]))
        g_cn2_ind = all_edges.index(ordered([i,j,2]))
        g_cn3_ind = all_edges.index(ordered([i,j,3]))
        mod.addConstr(sum(x[ordered([i,j,t])] for t in range(1,4))+g[g_cn1_ind]+g[g_cn2_ind]+g[g_cn3_ind]>=1)
        
        if g[g_cn1_ind]==0 or g[g_cn2_ind]==0 or g[g_cn3_ind]==0:
            mod.addConstr(sum(x[ordered([i,j,t])] for t in range(1,4))>=1)
        
        
        g_cn4_ind = all_edges.index(ordered([j,k,1]))
        g_cn5_ind = all_edges.index(ordered([j,k,2]))
        g_cn6_ind = all_edges.index(ordered([j,k,3]))
        mod.addConstr(sum(x[ordered([j,k,t])] for t in range(1,4))+g[g_cn4_ind]+g[g_cn5_ind]+g[g_cn6_ind]>=1)
        
        if g[g_cn4_ind]==0 or g[g_cn5_ind]==0 or g[g_cn6_ind]==0:
            mod.addConstr(sum(x[ordered([j,k,t])] for t in range(1,4))>=1)
        
        g_cn7_ind = all_edges.index(ordered([i,k,1]))
        g_cn8_ind = all_edges.index(ordered([i,k,2]))
        g_cn9_ind = all_edges.index(ordered([i,k,3]))
        mod.addConstr(sum(x[ordered([i,k,t])] for t in range(1,4))+g[g_cn7_ind]+g[g_cn8_ind]+g[g_cn9_ind]>=1)
        
        if len(connected_orient['%s_%s_%s'%(i,j,k)])>0:
            mod.addConstr(sum(x[ordered([i,j,t])] for t in range(1,4))+sum(x[ordered([j,k,t])] for t in range(1,4))+sum(x[ordered([i,k,t])] for t in range(1,4))>=1)
        
        if g[g_cn7_ind]==0 or g[g_cn8_ind]==0 or g[g_cn9_ind]==0:
            mod.addConstr(sum(x[ordered([i,k,t])] for t in range(1,4))>=1)
    
        if len(connected_orient['%s_%s_%s'%(i,j,k)])>0:
           mod.addConstr(sum(x[ordered([i,j,t])] for t in range(1,4))+sum(x[ordered([j,k,t])] for t in range(1,4))+sum(x[ordered([i,k,t])] for t in range(1,4))>=1)
    
        
       
        
    for i in range(noVer):
        for j in range(i+1,noVer):
            for t in range(1,4):        
              g_ind = all_edges.index((i,j,t))
              mod.addConstr(x[i,j,t]<=1-g[g_ind])

        
          
    mod.setObjective(sum(x[i,j,t] for (i,j,t) in all_edges), GRB.MINIMIZE)   
        
    mod.update()
    mod.optimize()
    
    
    new_edges = []
    if mod.Status==2:
        for (i,j,t) in all_edges:
            if x[i,j,t].x==1:
                new_edges.append([i,-t,j])
    else:
        sys.exit    
    edges.extend(new_edges)
    
 
    
    return(new_edges, edges,g)
        
        
        
      