import functools as fc

import matplotlib.animation as animation

from melkman import *
from utils import *
from gen_points import gen


class GrahamVisualiser:
    def __init__(self, points=None, interval=1000):
        self.hull_x = []
        self.hull_y = []
        self.hull = None
        self.start = None
        self.ax = None
        self.points = points
        self.interval = interval

    @staticmethod
    def compare(x, y, fst):
        return turn(fst, y, x) or dist(x, fst) - dist(y, fst)

    def init(self):
        self.ax.set_xlim(0, 15)
        self.ax.set_ylim(0, 15)
        self.hull.set_data(self.hull_x, self.hull_y)
        return self.hull, self.start

    def run(self, data):
        self.hull.set_data(self.hull_x, self.hull_y)
        return self.hull, self.start

    def grahamscan(self):
        n = len(self.points)  # число точек
        for i in range(1, n):
            # если P[i]-ая точка лежит ниже P[0]-ой точки,
            # меняем местами номера этих точек
            if self.points[i][1] < self.points[0][1] or self.points[i][1] == self.points[0][1] and self.points[i][0] > \
                    self.points[0][0]:
                self.points[i], self.points[0] = self.points[0], self.points[i]
        start = self.points.pop(0)
        self.start.set_data([start[0]], [start[1]])
        self.points.sort(key=fc.cmp_to_key(fc.partial(GrahamVisualiser.compare, fst=start)))
        self.hull_x.append(start[0])
        self.hull_y.append(start[1])
        yield None
        st = [start, self.points[0]]  # создаем стек
        self.hull_x.append(st[-1][0])
        self.hull_y.append(st[-1][1])
        yield None
        for i in range(1, n - 1):
            while len(st) >= 2 and turn(st[-2], st[-1], self.points[i]) == TURN_RIGHT:
                del st[-1]  # pop(S)
                del self.hull_x[-1]
                del self.hull_y[-1]
                yield None
            st.append(self.points[i])  # push(S,P[i])
            self.hull_x.append(self.points[i][0])
            self.hull_y.append(self.points[i][1])
            yield None
        self.hull_x.append(start[0])
        self.hull_y.append(start[1])
        yield None

    def visualise(self):
        fig, self.ax = plt.subplots()
        self.hull, = self.ax.plot([], [], 'o-', color='#00ff00', lw=3)
        self.ax.scatter([p[0] for p in self.points], [p[1] for p in self.points], color='black', lw=1)
        self.start, = self.ax.plot([], [], 'o', color='blue', lw=4)
        ani = animation.FuncAnimation(fig, self.run, self.grahamscan, init_func=self.init,
                                      blit=True, repeat=False, interval=self.interval)
        return ani


GrahamVisualiser(points=gen()).visualise()
