from utils import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class JarvisVisualiser:
    def __init__(self, ps, interval):
        self.interval = interval
        self.start = None
        self.cur_hull = None
        self.edge_candidate = None
        self.cur_edge = None
        self.points = ps
        self.start_pt_x = []
        self.start_pt_y = []
        self.hull_x = []
        self.hull_y = []
        self.edge_candidate_x = []
        self.edge_candidate_y = []
        self.cur_edge_x = []
        self.cur_edge_y = []

    def init(self):
        min_pt = min(self.points)
        self.hull_x.append(min_pt[0])
        self.hull_y.append(min_pt[1])
        self.start_pt_x.append(min_pt[0])
        self.start_pt_y.append(min_pt[1])
        self.start.set_data(self.start_pt_x, self.start_pt_y)
        self.cur_hull.set_data(self.hull_x, self.hull_y)
        return self.cur_hull, self.start, self.edge_candidate, self.cur_edge

    def run(self, data):
        self.cur_hull.set_data(self.hull_x, self.hull_y)
        self.start.set_data(self.start_pt_x, self.start_pt_y)
        self.edge_candidate.set_data(self.edge_candidate_x, self.edge_candidate_y)
        self.cur_edge.set_data(self.cur_edge_x, self.cur_edge_y)
        return self.cur_hull, self.start, self.edge_candidate, self.cur_edge

    def convex_hull(self):
        hull = [[self.hull_x[0], self.hull_y[0]]]
        # строим выпуклую оболочку и возвращаем точки в порядке обхода против часовой стрелки
        for p in hull:
            q = p
            self.edge_candidate_x.extend([q[0], q[0]])
            self.edge_candidate_y.extend([q[1], q[1]])
            self.cur_edge_x.extend([q[0], q[0]])
            self.cur_edge_y.extend([q[1], q[1]])
            yield None
            for r in self.points:
                self.cur_edge_x[1] = r[0]
                self.cur_edge_y[1] = r[1]
                yield None
                if r != p and (q == p or angle_less(p, q, r)):
                    q = r
                    self.edge_candidate_x[1] = q[0]
                    self.edge_candidate_y[1] = q[1]
                    yield None
            if q != hull[0]:
                hull.append(q)
            self.hull_x.append(q[0])
            self.hull_y.append(q[1])
            self.edge_candidate_x.clear()
            self.edge_candidate_y.clear()
            self.cur_edge_x.clear()
            self.cur_edge_y.clear()
            yield None

    def visualise(self):
        fig, ax = plt.subplots()
        point_xs, point_ys = [p[0] for p in self.points], [p[1] for p in self.points]
        ax.set_xlim(min(point_xs) - 2, max(point_xs) + 2)
        ax.set_ylim(min(point_ys) - 2, max(point_ys) + 2)
        self.start, = ax.plot(self.start_pt_x, self.start_pt_y, 'bo', lw=8)
        self.cur_hull, = ax.plot([], [], 'o-', color='#00ff00', lw=3)
        self.edge_candidate, = ax.plot([], [], 'o--', color='#00ff00', lw=3)
        self.cur_edge, = ax.plot(self.cur_edge_x, self.cur_edge_y, 'ok-', lw=3)
        ax.scatter(point_xs, point_ys, 'ok')
        ani = animation.FuncAnimation(fig, self.run, self.convex_hull, init_func=self.init, blit=True, repeat=False,
                                      interval=self.interval)
        return ani
