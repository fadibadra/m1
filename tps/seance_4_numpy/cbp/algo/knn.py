
def similarites(x, X, sim):
    similarites = []
    for i in range(len(X)):
        xi = X[i]
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

from decimal import Decimal, ROUND_HALF_UP
def round_up(num):
    return int(Decimal(num).quantize(Decimal('1'), rounding=ROUND_HALF_UP))

def vote_majoritaire(classes_des_voisins):
    vote = None
    moy = sum(classes_des_voisins)/len(classes_des_voisins)
    vote = round_up(moy)
    return vote

def predict(x, X, y, sim, n_neighbors=3):
    res = None
    # <- completer ici

    (_, indices) = tri_bulle(similarites(x, X, sim))

    kppv = indices[::-1][:n_neighbors]
    classes_des_voisins = [y[i] for i in kppv]
    res = vote_majoritaire(classes_des_voisins)

    return res