
import numpy as np

def vote_majoritaire(classes_des_voisins):
    classes, counts = np.unique(classes_des_voisins,return_counts=True)
    return classes[np.argmax(counts)]   

def predict(x, X, y, sim, n_neighbors=3):
    similarites = sim(x,X)
    indices = np.argsort(similarites)
    kppv = indices[::-1][:n_neighbors]
    classes_des_voisins = y[kppv]
    return vote_majoritaire(classes_des_voisins)
