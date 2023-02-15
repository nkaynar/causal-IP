#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Read independence/dependence relations
"""

import json
import os
import subprocess
import pandas as pd
import pdb


def conflicted_indep(noVer):
    
    S_all = {}
    C_all = {}
    subprocess.call("Rscript --vanilla ../ASP_schoolData_logweights/hyttinen2014uai_ver6/pkg/run_test.R %d"%noVer, shell=True)
    
    
    with open('../ASP_schoolData_logweights/hyttinen2014uai_ver6/pkg/R/export.JSON') as f:
        data = json.load(f)
            
    pdb.set_trace()
    tot_weight = 0
    weight_indep = {}
    weight_dep = {}                 
    for ii in range(len(data)):
          this_nodes = data[ii]['vars']
          this_key = '%s_%s'%(this_nodes[0]-1 ,this_nodes[1]-1)
          this_c = data[ii]['C']
          if not isinstance(this_c, list):
              this_c = [this_c]
              
          this_w = data[ii]['w']
          tot_weight = tot_weight+this_w
          #if list(data[ii]['independent'].values())[0]:
          if data[ii]['independent']:
              if this_key in S_all.keys():
                  weight_indep[this_key].append(this_w)
                  S_all[this_key].append([x - 1 for x in this_c])
              else:
                  S_all[this_key] = [[x - 1 for x in this_c]]
                  weight_indep[this_key] = [this_w]
          else:
              if this_key in C_all.keys():
                  weight_dep[this_key].append(this_w)
                  C_all[this_key].append([x - 1 for x in this_c])
              else:
                  C_all[this_key] = [[x - 1 for x in this_c]]
                  weight_dep[this_key] = [this_w]
                  
                  

          

    S_all_sorted =  {}
    C_all_sorted = {}
    weight_indep_sorted = {}
    weight_dep_sorted = {}
     
    for this_key in S_all.keys():
         for length in range(len(max(S_all[this_key],key=len))+1):
            s_subset = [this_c for this_c in S_all[this_key] if len(this_c)==length]  
            s_subset_true_ind = [this_n for this_n in range(len(S_all[this_key])) if len(S_all[this_key][this_n])==length]  
            
            # do this before sorting! 
            s_subset_sortinds = sorted(range(len(s_subset)), key=s_subset.__getitem__) 
            
            s_subset = sorted(s_subset)
            if this_key in S_all_sorted.keys():
                S_all_sorted[this_key].extend(s_subset)
                weight_indep_sorted[this_key].extend([weight_indep[this_key][s_subset_true_ind[i]] for i in s_subset_sortinds])
            else:
                S_all_sorted[this_key] = s_subset
                weight_indep_sorted[this_key] = [weight_indep[this_key][s_subset_true_ind[i]] for i in s_subset_sortinds]
                
                
    for this_key in C_all.keys():
         for length in range(len(max(C_all[this_key],key=len))+1):
            s_subset = [this_c for this_c in C_all[this_key] if len(this_c)==length]  
            s_subset_true_ind = [this_n for this_n in range(len(C_all[this_key])) if len(C_all[this_key][this_n])==length]  
            
            # do this before sorting! 
            s_subset_sortinds = sorted(range(len(s_subset)), key=s_subset.__getitem__) 
            s_subset = sorted(s_subset)
            if this_key in C_all_sorted.keys():
                C_all_sorted[this_key].extend(s_subset)
                weight_dep_sorted[this_key].extend([weight_dep[this_key][s_subset_true_ind[i]] for i in s_subset_sortinds])
            else:
                C_all_sorted[this_key] = s_subset  
                weight_dep_sorted[this_key] = [weight_dep[this_key][s_subset_true_ind[i]] for i in s_subset_sortinds]
                
    S = S_all_sorted
    C = C_all_sorted
    
    
    return(S,C,weight_indep_sorted,weight_dep_sorted)