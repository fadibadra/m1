import math

def euclidean_sim(a,b):
    res = 0.
    for i in range(len(a)):
        res = res + (a[i] - b[i])**2
    res = math.exp(-math.sqrt(res))
    return res

def dot(a,b):
    r = 0.
    for xi,yi in zip(a,b):
        r+=xi*yi
    return r

def norm(a):
    r = 0.
    for ai in a:
        r+=ai*ai
    return math.sqrt(r)

def cosin(a,b):
    return dot(a,b)/(norm(a)*norm(b))

def angle(c):
    return math.acos(c)/math.pi*180