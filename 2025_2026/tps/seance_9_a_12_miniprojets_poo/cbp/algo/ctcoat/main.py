import numpy as np
from itertools import combinations,permutations
from cbp.algo.ctcoat.simmatrix import simmatrix

# Class membership similarity. 
equal = lambda x,y: (True if x == y else False)

def not_k_neighbors(s, k):
    """Finds the instances that are NOT among the k nearest neighbors of the last instance."""
    # return np.argsort(s[len(s) - 1])[: -k - 1]
    return np.argsort(s[len(s) - 1][:-1])[:-k]

""" A continuous version of the CoAT case-based prediction algorithm. """

# def _add(st, rt, X, y, s, o):
#     return (np.vstack((X,st)), np.append(y, rt), s.add(st), o.add(rt))

# def _delete(k, X, y, s, o):
#     if k<0:
#         k = len(s) + k
#     return (np.delete(X, k, axis=0),np.delete(y, k), s.delete(k), o.delete(k))


def predict(x, X, y, sim_X, sim_y=equal, n_neighbors=None, return_energies=False):
    """ Predicts the outcome for x given the case base (X,y) and the similarity measures sim_X and sim_y. """
    if type(X) is list:
        X = np.array(X)
    if type(y) is list:
        y = np.array(y)

    potential_outcomes = np.unique(np.array(y))
    s = simmatrix(X, sim_X)
    o = simmatrix(y, sim_y)
    if n_neighbors is not None:
        unwanted = not_k_neighbors(s.add(x), n_neighbors)
        s = s.delete(unwanted)
        o = o.delete(unwanted)
    min_outcome = potential_outcomes[0]
    (s,o) = (s.add(x), o.add([min_outcome]))
    i = s.shape[0] - 1
    min_energy = energy_increase(i,s,o)
    if return_energies:
            energies = [min_energy]
    for r in potential_outcomes[1:]:
        if type(o.df[i]) is np.ndarray:
            o.df[i,] = r
        else:
            o.df[i] = r
        o.fill_column(i)
        o.fill_row(i)
        e = energy_increase(i,s,o)
        if return_energies:
            energies.append(e)
        if e < min_energy:
            min_energy = e
            min_outcome = r
    if return_energies:
        return (energies, min_outcome)
    else:
        return min_outcome


def energy_increase(k, s, o):
        """ The energy increase for the n*n+(n-1)(2n-1) inversions which instance k takes part of. """
        n = len(s)
        if k < 0:
            k = n + k
        r = 0.
        not_k = list(range(n))
        not_k.remove(k)

        # k i j
        for (i,j) in combinations(not_k,2):
            r += (1 - (s[k][i]-s[k][j])*(o[k][i]-o[k][j]))
        
        # k i i
        r += (n-1) / 2

        # k k i et k i k 
        for i in not_k:
            r += (1 - (s[k][k]-s[k][i])*(o[k][k]-o[k][i]))

        # k k k 
        r += 1/2

        # i k k
        r += (n-1)/2
        
        # i k j et i j k
        for (i,j) in permutations(not_k,2):
            r += (1 - (s[i][k]-s[i][j])*(o[i][k]-o[i][j]))

        # i k i and i i k
        for i in not_k:
            r += (1 - (s[i][i]-s[i][k])*(o[i][i]-o[i][k]))

        return r