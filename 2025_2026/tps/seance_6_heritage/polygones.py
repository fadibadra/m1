import matplotlib.pyplot as plt
import numpy as np
from abc import ABC, abstractmethod

class Figure(ABC):

    @abstractmethod
    def dessine_sur(self, ax):
        pass

class Point(Figure):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dessine_sur(self, ax):
        ax.plot([self.x], [self.y], 'o', lw=2)[0]

    def __repr__(self):
        return f'({self.x}, {self.y})'

class Polygone(list[Point],Figure):

        marker = '-'
        lw = 2
        couleur = 'blue'

        def dessine_sur(self, ax):
            (x,y) = ([e.x for e in self], [e.y for e in self])  
            ax.plot(x, y, Polygone.marker, lw=Polygone.lw, c=Polygone.couleur)[0]

class Carre(Polygone):
    def __init__(self, centre, r):
        x_c,y_c = centre
        self.append(Point(x_c+r/2,y_c+r/2))
        self.append(Point(x_c-r/2,y_c+r/2))
        self.append(Point(x_c-r/2,y_c-r/2))
        self.append(Point(x_c+r/2,y_c-r/2))
        self.append(Point(x_c+r/2,y_c+r/2))

class VonKoch(Polygone):
    def __init__(self, *args, n_iter=3):
        super().__init__(*args)
        for _ in range(n_iter):
            self._decompose()

    def _decompose(self):
        n = self.__len__()
        i = n 
        while i>1:
            u,v = self[i-2:i]
            a = np.array([u.x,u.y])
            b = np.array([v.x,v.y])
            new_u = a + (b-a)/3
            new_v = a + 2*(b-a)/3
            theta = np.pi/3
            rot = np.array([[np.cos(theta), -np.sin(theta)],[np.sin(theta), np.cos(theta)]])
            new_w = new_u + rot @ (new_v-new_u)
            self.insert(i-1,Point(*list(new_v)))
            self.insert(i-1,Point(*list(new_w)))
            self.insert(i-1,Point(*list(new_u)))
            i = i - 1

class Dessin(object):

    def __init__(self):
        fig = plt.figure(figsize=(10, 10),dpi=72)
        ax = fig.add_subplot(xlim=(-10,10),ylim=(-10,10))
        ax.set_aspect('equal')
        ax.set_axis_off()
        self.fig = fig
        self.ax = ax

    def dessine(self, p):
        p.dessine_sur(self.ax)

