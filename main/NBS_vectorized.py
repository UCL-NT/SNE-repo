from __future__ import division
import numpy as np
import math
from scipy import stats
from sklearn.utils.validation import check_random_state


'''
Adopted from vectorized NBS in the python implementation from Gideon Rosenthal
Referenced: Zalesky A, Fornito A, Bullmore ET (2010) 

'''     

def partial_corr(x, y, control):
    
    rxy = stats.spearmanr(x, y)[0]
    ryc = stats.spearmanr(y, control)[0]
    rxc = stats.spearmanr(x, control)[0]

    p_cor = (rxy-ryc*rxc)/(math.sqrt(1-ryc**2)*math.sqrt(1-rxc**2))
        
    return p_cor

def nbs_corr(data_matrix, y_vec, cov, k=10000):
    """
    Simplified vectorized network-based correlation analysis.
    
    Parameters:
    -----------
    data_matrix : numpy.ndarray
        Input matrix of shape N x P (N variables, P subjects)
    y_vec : numpy.ndarray
        Behavioral/physiological vector of length P
    k : int, optional
        Number of permutations (default 10000)
    
    Returns:
    --------
    pvals : numpy.ndarray
        p-values for each edge
    true_r : numpy.ndarray
        True correlation values for each edge
    """
    # Get dimensions
    n = data_matrix.shape[0]
    
    # Validate input
    if len(y_vec) != data_matrix.shape[1]:
        raise ValueError("Length of y_vec must match second dimension of data_matrix")
    
    # Compute true correlations
    true_r = np.zeros(n)
    for i in range(n):
        true_r[i] = partial_corr(data_matrix[i, :], y_vec,cov)
        print(true_r[i])
    
    # Fisher z-transform
    true_z = np.arctanh(true_r)
    rs = check_random_state(0)
    # Permutation
    null_dist = 1
    pvals = np.zeros(n)
    for j in range(n):
        ap = data_matrix[j, :]
        for i in range(k):
            perm_x = ap[rs.permutation(len(ap))]
            perm_y = y_vec[rs.permutation(len(y_vec))]
            perm_r = partial_corr(perm_x, perm_y,cov)
            null_dist += np.arctanh(np.abs(perm_r)) >= np.abs(true_z[j])
        
        pvals[j] = null_dist/k
        null_dist = 1
    
    return pvals, true_r


