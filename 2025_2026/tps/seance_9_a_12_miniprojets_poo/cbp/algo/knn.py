import numpy as np 
def vote_majoritaire(classes_des_voisins):
    counts = {}
    for c in classes_des_voisins:
        if c not in counts:
            counts[c] = 0
        else:
            counts[c] += 1
    return max(counts, key=counts.get)

def kneighbors(x, X_cb, sim, n_neighbors=3, return_similarities=False):
    similarites = sim(x, X_cb)
    indices = np.argsort(similarites)
    sim_values = similarites[indices]
    kppv = indices[::-1][:n_neighbors]
    if return_similarities:
        return (kppv, sim_values[::-1][:n_neighbors])
    else:
        return kppv

def predict(x, X_cb, y_cb, sim, n_neighbors=3):
    indices = kneighbors(x, X_cb, sim, n_neighbors=n_neighbors)
    kppv = indices[::-1][:n_neighbors]
    classes_des_voisins = y_cb[kppv]
    return vote_majoritaire(classes_des_voisins)
