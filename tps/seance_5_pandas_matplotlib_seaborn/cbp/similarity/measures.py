import numpy as np
from numpy.linalg import norm

def euclidean_sim(a,b):
    return np.exp(-norm(a-b,axis=1))

def cosin(a,b):
    return np.dot(a,b)/(norm(a)*norm(b))

