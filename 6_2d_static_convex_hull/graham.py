import functools as fc

import matplotlib.animation as animation

from utils import *


class GrahamVisualiser:
    def __init__(self, points=None, interval=1000):
        self.data_current = [[], []]
        self.hull_x = []
        self.hull_y = []
        self.deleted_x = []
        self.deleted_y = []
        self.current = None
        self.hull = None
        self.start = None
        self.ax = None
        self.deleted = None
        self.points = points
        self.interval = interval

    @staticmethod
    def compare(x, y, fst):
        return turn(fst, y, x) or dist(x, fst) - dist(y, fst)

    def init(self):
        point_xs, point_ys = [p[0] for p in self.points], [p[1] for p in self.points]
        self.ax.set_xlim(min(point_xs) - 2, max(point_xs) + 2)
        self.ax.set_ylim(min(point_ys) - 2, max(point_ys) + 2)
        self.hull.set_data(self.hull_x, self.hull_y)
        self.deleted.set_data(self.deleted_x, self.deleted_y)
        return self.hull, self.start, self.deleted

    def run(self, data):
        self.hull.set_data(self.hull_x, self.hull_y)
        self.deleted.set_data(self.deleted_x, self.deleted_y)
        self.current.set_data(*self.data_current)
        return self.hull, self.start, self.deleted, self.current

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
            self.data_current[0].clear()
            self.data_current[1].clear()
            self.data_current[0].append(self.points[i][0])
            self.data_current[1].append(self.points[i][1])
            yield None
            while len(st) >= 2 and turn(st[-2], st[-1], self.points[i]) == TURN_RIGHT:
                del st[-1]  # pop(S)
                self.deleted_x.append(self.hull_x.pop())
                self.deleted_y.append(self.hull_y.pop())
                self.deleted_x.append(st[-1][0])
                self.deleted_y.append(st[-1][1])
                yield None
            self.deleted_x.clear()
            self.deleted_y.clear()
            st.append(self.points[i])  # push(S,P[i])
            self.hull_x.append(self.points[i][0])
            self.hull_y.append(self.points[i][1])
            yield None
        self.hull_x.append(start[0])
        self.hull_y.append(start[1])
        yield None
        self.data_current[0].clear()
        self.data_current[1].clear()
        yield None

    def visualise(self):
        fig, self.ax = plt.subplots()

        self.hull, = self.ax.plot([], [], 'go-', lw=3)
        self.ax.scatter([p[0] for p in self.points], [p[1] for p in self.points], color='black', lw=1)
        self.start, = self.ax.plot([], [], 'bo', lw=4)
        self.deleted, = self.ax.plot([], [], 'ro-', lw=3)
        self.current, = self.ax.plot([], [], 'o',  color='#00ff00', lw=3)
        ani = animation.FuncAnimation(fig, self.run, self.grahamscan, init_func=self.init,
                                      blit=True, repeat=False, interval=self.interval, save_count=1000)
        # plt.draw()
        # plt.show()
        return ani


# GrahamVisualiser(points=gen()).visualise()
