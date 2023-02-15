#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Call ASP and get results
"""

from oracle_ASP import getIndepRelations
import subprocess
import pandas as pd
from getError import computeError
import numpy as np
import pdb
from test_conflicted import conflicted_indep


def conflicted_ASP(noVer):
    
    if noVer<15:
    
        subprocess.call ("Rscript --vanilla ../ASP/hyttinen2014uai_ver6/pkg/run_test.R %d"%noVer, shell=True)
        #save underlying graph
        D_true_asp = pd.read_csv('../ASP/hyttinen2014uai_ver6/pkg/R/true_D.csv', index_col='Unnamed: 0')
        E_true_asp = pd.read_csv('../ASP/hyttinen2014uai_ver6/pkg/R/true_E.csv', index_col='Unnamed: 0')
        S_true_asp, C_true_asp = getIndepRelations(D_true_asp,E_true_asp)
        
       
       
        
        #save estimated graph by ASP
        D_est_asp = pd.read_csv('../ASP/hyttinen2014uai_ver6/pkg/R/est_D.csv', index_col='Unnamed: 0')
        E_est_asp = pd.read_csv('../ASP/hyttinen2014uai_ver6/pkg/R/est_E.csv', index_col='Unnamed: 0')
        S_est_asp, C_est_asp = getIndepRelations(D_est_asp,E_est_asp)
        
        ASP_error = computeError(S_true_asp,C_true_asp,S_est_asp, C_est_asp)
        
        S,C,we_s,we_c = conflicted_indep(noVer)
        true_ASP_loss = computeError(S_est_asp,C_est_asp,S, C)
        
        weighted_ASP_loss = 0
        for tt_key in S.keys():
            for t_n,t_c in enumerate(S[tt_key]):
                if tt_key in S_est_asp.keys() and t_c not in S_est_asp[tt_key]:
                    weighted_ASP_loss = weighted_ASP_loss + we_s[tt_key][t_n]
                    
        for tt_key in C.keys():
            for t_n,t_c in enumerate(C[tt_key]):
                if tt_key in C_est_asp.keys() and t_c not in C_est_asp[tt_key]:
                    weighted_ASP_loss = weighted_ASP_loss + we_c[tt_key][t_n]
               
                    
                
        
        
       
        
        this_ASP = np.loadtxt('../ASP/hyttinen2014uai_ver6/pkg/R/solving_time.txt').tolist()
     
        
        if np.isinf(this_ASP):
            with open('../ASP/hyttinen2014uai_ver6/pkg/tmp/pipeline.ind.clingo') as f:
                load_success = False
                for line in f:
                    if line.startswith('Optimization :'):
                        this_obj_ASP = int(line.strip().split(' : ')[1])
                        load_success = True
                        break
            assert load_success, "could not read 'this_obj_ASP'!"
            
            this_ASP = 3600
        else:
            this_ASP = np.loadtxt('../ASP/hyttinen2014uai_ver6/pkg/R/solving_time.txt').tolist()
            this_obj_ASP = np.loadtxt('../ASP/hyttinen2014uai_ver6/pkg/R/objective.txt').tolist()
            
    else:
        
        subprocess.call ("Rscript --vanilla ../ASP_conflict_IP/hyttinen2014uai_ver6/pkg/run_test.R %d"%noVer, shell=True)
        
        #save underlying graph
        D_true_asp = pd.read_csv('../ASP_conflict_IP/hyttinen2014uai_ver6/pkg/R/true_D.csv', index_col='Unnamed: 0')
        E_true_asp = pd.read_csv('../ASP_conflict_IP/hyttinen2014uai_ver6/pkg/R/true_E.csv', index_col='Unnamed: 0')
        S_true_asp, C_true_asp = getIndepRelations(D_true_asp,E_true_asp)
           
    
        
        
    if noVer<15:    
        return(ASP_error,this_obj_ASP,this_ASP, S_true_asp, C_true_asp,D_true_asp,E_true_asp,D_est_asp,E_est_asp,true_ASP_loss,weighted_ASP_loss)
    
    else:        
        return(S_true_asp, C_true_asp,D_true_asp,E_true_asp)
        
        
        
        
        
        
        
        
        
        
        
        
