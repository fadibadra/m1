import numpy as np
from numpy.linalg import norm

def euclidean_sim(a,b):
    return np.exp(-norm(a-b,axis=max(a.ndim - 1, b.ndim - 1)))

def cosin(a,b):
    if len(a.shape) == 1:
        a = np.expand_dims(a,0)
    if len(b.shape) == 1:
        b = np.expand_dims(b,0)
    a_unit = a / norm(a,axis=1)[:,None]
    b_unit = b / norm(b,axis=1)[:,None]
    return np.sum(a_unit*b_unit, axis=1)
