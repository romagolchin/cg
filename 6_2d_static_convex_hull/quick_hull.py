import matplotlib.animation as animation
from utils import *


class QuickHullVisualiser:
    def __init__(self, points=None, interval=1000):
        self.points = points
        self.interval = interval
        self.main_edge = None
        self.cur_edge = None
        self.edge_stack = None
        self.hull_edges = None
        self.hull = None
        self.data_main_edge = [[], []]
        self.data_cur_edge = [[], []]
        self.data_edge_stack = [[], []]
        self.data_hull_edges = [[], []]
        self.data_hull = [[], []]

    def init(self):
        return self.run(None)

    def run(self, data):
        # self.main_edge.set_data(*self.data_main_edge)
        self.cur_edge.set_data(*self.data_cur_edge)
        self.edge_stack.set_data(*self.data_edge_stack)
        self.hull_edges.set_data(*self.data_hull_edges)
        self.hull.set_data(*self.data_hull)
        return self.main_edge, self.cur_edge, self.edge_stack, self.hull_edges, self.hull

    def get_hull_points(self):
        min_pt, max_pt = QuickHullVisualiser.get_min_max_x(self.points)
        self.data_hull[0].extend([min_pt[0], max_pt[0]])
        self.data_hull[1].extend([min_pt[1], max_pt[1]])
        yield None
        self.data_main_edge = [[min_pt[0], max_pt[0]], [min_pt[1], max_pt[1]]]
        yield None
        hull_pts = None
        for pts in self.quick_hull(self.points, min_pt, max_pt):
            if pts is None:
                yield pts
            else:
                hull_pts = pts
        for pts in self.quick_hull(self.points, max_pt, min_pt):
            if pts is None:
                yield pts
            else:
                hull_pts += pts
                self.data_hull_edges[0] = [p[0] for p in hull_pts] + [hull_pts[0][0]]
                self.data_hull_edges[1] = [p[1] for p in hull_pts] + [hull_pts[0][1]]
                yield hull_pts
                # self.data_hull[0].append(self.data_hull[0][0])
                # self.data_hull[1].append(self.data_hull[1][0])
                # yield None

    def quick_hull(self, points, min_pt, max_pt):
        self.data_cur_edge = [[min_pt[0], max_pt[0]], [min_pt[1], max_pt[1]]]
        yield None
        left_of_line_pts = QuickHullVisualiser.get_points_left_of_line(min_pt, max_pt, points)
        pt_c = QuickHullVisualiser.point_max_from_line(min_pt, max_pt, left_of_line_pts)
        if pt_c is None:
            yield [max_pt]
        else:
            self.data_hull[0].append(pt_c[0])
            self.data_hull[1].append(pt_c[1])
            yield None
            self.data_edge_stack[0] += self.data_cur_edge[0]
            self.data_edge_stack[1] += self.data_cur_edge[1]
            yield None
            hull_pts = None
            for pts in self.quick_hull(left_of_line_pts, min_pt, pt_c):
                if pts is None:
                    yield pts
                else:
                    hull_pts = pts
            for pts in self.quick_hull(left_of_line_pts, pt_c, max_pt):
                if pts is None:
                    yield pts
                else:
                    hull_pts += pts
                    # for p in hull_pts:
                    #     self.data_hull[0].append(p[0])
                    #     self.data_hull[1].append(p[1])
                    yield hull_pts
            self.data_edge_stack[0].pop()
            self.data_edge_stack[0].pop()
            self.data_edge_stack[1].pop()
            self.data_edge_stack[1].pop()
            yield None

    @staticmethod
    def get_points_left_of_line(start, end, points):
        pts = []
        for pt in points:
            if turn(start, end, pt) == TURN_RIGHT:
                pts.append(pt)

        return pts

    @staticmethod
    def point_max_from_line(start, end, points):
        max_dist = 0

        max_point = None

        for point in points:
            if point != start and point != end:
                dist = QuickHullVisualiser.distance(start, end, point)
                if dist > max_dist:
                    max_dist = dist
                    max_point = point

        return max_point

    @staticmethod
    def get_min_max_x(list_pts):
        min_x = float('inf')
        max_x = 0
        min_y = 0
        max_y = 0

        for x, y in list_pts:
            if x < min_x:
                min_x = x
                min_y = y
            if x > max_x:
                max_x = x
                max_y = y

        return [min_x, min_y], [max_x, max_y]

    # расстояние от pt до прямой, проходящей через start и end
    # расстояние пропорционально площади треугольника построенного на  start, end, pt
    # (так как является его высотой), а площадь равна модулю поворота / 2
    @staticmethod
    def distance(start, end, pt):
        return abs(turn_value(start, end, pt))

    def visualise(self):
        fig, ax = plt.subplots()
        point_xs, point_ys = [p[0] for p in self.points], [p[1] for p in self.points]
        ax.set_xlim(min(point_xs) - 2, max(point_xs) + 2)
        ax.set_ylim(min(point_ys) - 2, max(point_ys) + 2)
        ax.scatter(point_xs, point_ys, color='black', lw=1)
        self.main_edge, = ax.plot([], [], 'r-', lw=3)
        self.cur_edge, = ax.plot([], [], 'k-', lw=3)
        self.edge_stack, = ax.plot([], [], color='#00ff00', lw=1)
        self.hull_edges, = ax.plot([], [], 'go-', lw=3, ms=5)
        self.hull, = ax.plot([], [], 'go', lw=0, ms=5)
        ani = animation.FuncAnimation(fig, self.run, self.get_hull_points, init_func=self.init,
                                      interval=self.interval, blit=True, repeat=False, save_count=1000)
        return ani


