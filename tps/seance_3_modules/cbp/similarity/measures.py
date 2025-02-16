import math

def euclidean_sim(a,b):
    res = 0.
    for i in range(len(a)):
        res = res + (a[i] - b[i])**2
    res = math.exp(-math.sqrt(res))
    return res

