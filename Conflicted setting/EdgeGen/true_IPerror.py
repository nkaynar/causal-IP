
"""
Computes error between true graph and a graph returned by EdgeGen

"""

import numpy as np
from getError import computeError
from oracle_ASP import getIndepRelations

def computeIPerror(D_est_int, E_est_int,S_true_asp,C_true_asp,noVer):
    vertices = list(range(noVer))
    D_est_IPASP = np.zeros((noVer, noVer), dtype=int)
    E_est_IPASP = -E_est_int

    for ii in vertices:
        for ii_2 in vertices:
            if D_est_int[ii, ii_2] == -2 or D_est_int[ii, ii_2] == -3:
                D_est_IPASP[ii, ii_2] = 1

    S_est_IP, C_est_IP = getIndepRelations(D_est_IPASP, E_est_IPASP)

    IP_error = computeError(S_true_asp, C_true_asp, S_est_IP, C_est_IP)
    return(IP_error)