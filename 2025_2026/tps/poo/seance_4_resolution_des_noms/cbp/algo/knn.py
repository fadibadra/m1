
def similarites(x, X_cb, sim):
    similarites = []
    for i in range(len(X_cb)):
        xi = X_cb[i]
        sim_i = sim(x,xi)
        similarites.append(sim_i)

    return similarites

def tri_bulle(tab):
    t = tab.copy()
    n = len(t)
    indices = list(range(n))
    echange = True
    i = 1
    while n-1-i>0 and echange:
        echange = False
        for j in range(0,n-i):
            if t[j]>t[j+1]:
                tmp = t[j+1]
                t[j+1] = t[j]
                t[j] = tmp
                tmp = indices[j+1]
                indices[j+1] = indices[j]
                indices[j] = tmp
                echange = True
        i = i + 1
    sorted_values = t
    return (sorted_values, indices)

def vote_majoritaire(classes_des_voisins):
    counts = {}
    for c in classes_des_voisins:
        if c not in counts:
            counts[c] = 0
        else:
            counts[c] = counts[c] + 1
    return max(counts, key=counts.get)

def kneighbors(x, X_cb, sim, n_neighbors=3, return_similarities=False):
    (sim_values, indices) = tri_bulle(similarites(x, X_cb, sim))
    kppv = indices[::-1][:n_neighbors]
    if return_similarities:
        return (kppv, sim_values[::-1][:n_neighbors])
    else:
        return kppv

def predict(x, X_cb, y_cb, sim, n_neighbors=3):
    res = None
    kppv = kneighbors(x, X_cb, sim, n_neighbors=n_neighbors)
    classes_des_voisins = [y_cb[i] for i in kppv]
    res = vote_majoritaire(classes_des_voisins)
    return res