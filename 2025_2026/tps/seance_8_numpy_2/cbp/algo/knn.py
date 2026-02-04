import numpy as np 

def similarites(x, X_cb, sim):
    return np.array([sim(x, xi) for xi in X_cb])

def kneighbors(x, X_cb, sim, n_neighbors=3, return_similarities=False):
    sim_values = similarites(x, X_cb, sim)
    indices = np.argsort(sim_values)
    ordered_sim_values = sim_values[indices]
    kppv = indices[::-1][:n_neighbors]
    if return_similarities:
        return (kppv, ordered_sim_values[::-1][:n_neighbors])
    else:
        return kppv
    
def vote_majoritaire(classes_des_voisins):
    classes, counts = np.unique(classes_des_voisins,return_counts=True)
    return classes[np.argmax(counts)]

def predict(x, X_cb, y_cb, sim, n_neighbors=3):
    kppv = kneighbors(x, X_cb, sim, n_neighbors=n_neighbors)
    classes_des_voisins = [y_cb[i] for i in kppv]
    res = vote_majoritaire(classes_des_voisins)
    return res
