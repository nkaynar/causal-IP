
"""
Compute S(z) and \bar{S}(z) part 2

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





def update_triple_orientation(collider_triple, noncollider_triple, col_noncol_triple, col_orient, noncol_orient, connected_orient,edges):
    

    remove_col_orient = {}  
    remove_noncol_orient = {} 
    remove_connected_orient = {}
                  
    for (i,j,k) in collider_triple:                            
        for this_orient in col_orient['%s_%s_%s'%(i,j,k)]:           
            if this_orient[0] in edges and this_orient[1] in edges:
                if '%s_%s_%s'%(i,j,k) in remove_col_orient.keys():
                    remove_col_orient['%s_%s_%s'%(i,j,k)].append(this_orient)
                else:
                    remove_col_orient['%s_%s_%s'%(i,j,k)] = [this_orient]

                
    for (i,j,k) in noncollider_triple:                            
        for this_orient in noncol_orient['%s_%s_%s'%(i,j,k)]:           
            if this_orient[0] in edges and this_orient[1] in edges:
                if '%s_%s_%s'%(i,j,k) in remove_noncol_orient.keys():
                    remove_noncol_orient['%s_%s_%s'%(i,j,k)].append(this_orient)
                else:
                    remove_noncol_orient['%s_%s_%s'%(i,j,k)] = [this_orient]
                
    
                
    for (i,j,k) in col_noncol_triple:                            
        for this_orient in connected_orient['%s_%s_%s'%(i,j,k)]:           
            if this_orient[0] in edges and this_orient[1] in edges and this_orient[2] in edges:
                
                if '%s_%s_%s'%(i,j,k) in remove_connected_orient.keys():
                    remove_connected_orient['%s_%s_%s'%(i,j,k)].append(this_orient)
                else:
                    remove_connected_orient['%s_%s_%s'%(i,j,k)] = [this_orient]
                    
    
    for this_key in remove_col_orient.keys(): 
        for this_orient in remove_col_orient[this_key]:
            col_orient[this_key].remove(this_orient)
                
    for this_key in remove_noncol_orient.keys():  
        for this_orient in remove_noncol_orient[this_key]:
            noncol_orient[this_key].remove(this_orient)
                
    for this_key in remove_connected_orient.keys(): 
        for this_orient in remove_connected_orient[this_key]:
            connected_orient[this_key].remove(this_orient)
  
                
    return(col_orient, noncol_orient, connected_orient)
     
    
    
    
    
    
    