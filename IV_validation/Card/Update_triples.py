
"""
Update S(z) and \bar{S}(z) 
"""



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


def update_triples(C_not, collider_triple, noncollider_triple, col_noncol_triple, col_orient, noncol_orient, connected_orient):
                         
    col_not  = []                  
    for (i,j,k) in collider_triple:
        if C_not['%s_%s'%tuple(sorted([i,k]))]!=[]: 
            if len(col_orient['%s_%s_%s'%(i,j,k)])>0:
                col_not.append([i,j,k])
                                                               
    noncol_not  = []
    for (i,j,k) in noncollider_triple:
        if C_not['%s_%s'%tuple(sorted([i,k]))]!=[]:                   
            if len(noncol_orient['%s_%s_%s'%(i,j,k)])>0:
                noncol_not.append([i,j,k])    

    col_noncol_not = []
    for (i,j,k) in col_noncol_triple:
        if C_not['%s_%s'%tuple(sorted([i,j]))]!=[]:
            if len(connected_orient['%s_%s_%s'%(i,j,k)])>0:
                col_noncol_not.append([i,j,k])
                
    return(col_not, noncol_not,col_noncol_not)
     
    
    
    
    
    
    