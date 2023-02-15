#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compute S(z) and \bar{S}(z) part 1
"""




import timeit
from itertools import combinations 



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





def generate_triples(noVer, S, C):
    
    no_edge = []
    pairs = list(combinations(range(noVer),2))
    triplets = list(combinations(range(noVer),3))
    pair_1 = [] # [i,j] if i?-->j
    pair_2 = [] 
    pair_3 = [] # [i,j] if i<-->j      
    noncollider_triple = []
    collider_triple = []
    col_noncol_triple = []
    connected_pairs = []
    
    
    for (i,j) in pairs:
        if not '%s_%s'%tuple(sorted([i,j])) in S.keys():
            connected_pairs.append([i,j])
        for k in set(list(range(noVer))).difference(set([i,j])):
            if '%s_%s'%(i,j) in S.keys() and '%s_%s'%tuple(sorted([i,k])) not in S.keys() and '%s_%s'%tuple(sorted([k,j])) not in S.keys() and not any(k in sublist for sublist in S['%s_%s'%(i,j)]):
                collider_triple.append([i,k,j])
                if not [i,k] in pair_1:
                    pair_1.append([i,k])
                if not [j,k] in pair_1:
                    pair_1.append([j,k])
            if '%s_%s'%(i,j) in S.keys() and '%s_%s'%tuple(sorted([i,k])) not in S.keys() and '%s_%s'%tuple(sorted([k,j])) not in S.keys() and all(k in sublist for sublist in S['%s_%s'%(i,j)]):
                noncollider_triple.append([i,k,j])
                if not [i,k] in pair_3:
                    pair_3.append([i,k])
                if not [k,j] in pair_3:
                    pair_3.append([k,j])
    for (i,j,k) in triplets:               
         if not '%s_%s'%tuple(sorted([i,j])) in S.keys() and not '%s_%s'%tuple(sorted([i,k])) in S.keys() and  not '%s_%s'%tuple(sorted([k,j])) in S.keys():
             col_noncol_triple.append([i,k,j])           
             col_noncol_triple.append([k,i,j])
             col_noncol_triple.append([i,j,k])
       
    edges = []   
    
    
    collider_triple.extend(col_noncol_triple)
    noncollider_triple.extend(col_noncol_triple)
    
    col_noncol_triple = []
    
    col_orient = {}        
    for (i,j,k) in collider_triple:                
        generic_col = [[ordered([i,-1,j]),ordered([j,-2,k])], [ordered([i,-1,j]),ordered([j,-3,k])], [ordered([i,-3,j]),ordered([j,-2,k])], [ordered([i,-3,j]),ordered([j,-3,k])]]
        correct_col_orient = []
        for this_orient in generic_col:               
            correct_col_orient.append(this_orient)
        col_orient['%s_%s_%s'%(i,j,k)] = correct_col_orient
    
        
        
    noncol_orient = {}         
    for (i,j,k) in noncollider_triple:                
        generic_noncol = [[ordered([i,-1,j]),ordered([j,-1,k])], [ordered([i,-2,j]),ordered([j,-1,k])], [ordered([i,-2,j]),ordered([j,-2,k])], [ordered([i,-2,j]),ordered([j,-3,k])], [ordered([i,-3,j]),ordered([j,-1,k])]]
        correct_noncol_orient = []
        for this_orient in generic_noncol:
            correct_noncol_orient.append(this_orient)
        noncol_orient['%s_%s_%s'%(i,j,k)] = correct_noncol_orient
        
        
    
    connected_orient = {}
    for (i,j,k) in col_noncol_triple: 
        correct_con_orient = []                              
        generic_con = [[ordered([i,-1,j]),ordered([j,-2,k]),ordered([i,-1,k])], [ordered([i,-1,j]),ordered([j,-3,k]),ordered([i,-1,k])], 
                       [ordered([i,-3,j]),ordered([j,-2,k]),ordered([i,-1,k])], [ordered([i,-3,j]),ordered([j,-3,k]),ordered([i,-1,k])],
                       [ordered([i,-1,j]),ordered([j,-1,k]),ordered([i,-1,k])], [ordered([i,-2,j]),ordered([j,-1,k]),ordered([i,-1,k])], 
                       [ordered([i,-2,j]),ordered([j,-2,k]),ordered([i,-1,k])], [ordered([i,-2,j]),ordered([j,-3,k]),ordered([i,-1,k])], 
                       [ordered([i,-3,j]),ordered([j,-1,k]),ordered([i,-1,k])]]   
        generic_con.extend([[ordered([i,-1,j]),ordered([j,-2,k]),ordered([i,-2,k])], [ordered([i,-1,j]),ordered([j,-3,k]),ordered([i,-2,k])], 
                       [ordered([i,-3,j]),ordered([j,-2,k]),ordered([i,-2,k])], [ordered([i,-3,j]),ordered([j,-3,k]),ordered([i,-2,k])],
                       [ordered([i,-1,j]),ordered([j,-1,k]),ordered([i,-2,k])], [ordered([i,-2,j]),ordered([j,-1,k]),ordered([i,-2,k])], 
                       [ordered([i,-2,j]),ordered([j,-2,k]),ordered([i,-2,k])], [ordered([i,-2,j]),ordered([j,-3,k]),ordered([i,-2,k])], 
                       [ordered([i,-3,j]),ordered([j,-1,k]),ordered([i,-2,k])]]  )     
        generic_con.extend([[ordered([i,-1,j]),ordered([j,-2,k]),ordered([i,-3,k])], [ordered([i,-1,j]),ordered([j,-3,k]),ordered([i,-3,k])], 
                       [ordered([i,-3,j]),ordered([j,-2,k]),ordered([i,-3,k])], [ordered([i,-3,j]),ordered([j,-3,k]),ordered([i,-3,k])],
                       [ordered([i,-1,j]),ordered([j,-1,k]),ordered([i,-3,k])], [ordered([i,-2,j]),ordered([j,-1,k]),ordered([i,-3,k])], 
                       [ordered([i,-2,j]),ordered([j,-2,k]),ordered([i,-3,k])], [ordered([i,-2,j]),ordered([j,-3,k]),ordered([i,-3,k])], 
                       [ordered([i,-3,j]),ordered([j,-1,k]),ordered([i,-3,k])]]  )                      
        for this_orient in generic_con:
            correct_con_orient.append(this_orient)            
        connected_orient['%s_%s_%s'%(i,j,k)] = correct_con_orient
   

  
    return(collider_triple,noncollider_triple, col_noncol_triple,edges,no_edge,col_orient,noncol_orient,connected_orient,connected_pairs)