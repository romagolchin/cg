from cg.utils import cmp_
from numpy import random as rnd
import matplotlib.pyplot as plt

TURN_LEFT, TURN_RIGHT, TURN_NONE = (1, -1, 0)


def turn(p, q, r):
    # предикат поворота, возвращает 1, -1, 0, если точки p, q, r  образуют левый, правый повороты
    # или лежат на одной прямой, соответственно.
    return cmp_(turn_value(p, q, r), 0)


def turn_value(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (r[0] - p[0]) * (q[1] - p[1])


def dist(q, p):
    # считаем квадрат расстояния
    dx, dy = q[0] - p[0], q[1] - p[1]
    return dx * dx + dy * dy


# верно ли, что r имеет меньший угол относительно p чем q или такой же,
# но удалена на меньшее расстояние от p
def angle_less(p, q, r):
    t = turn(p, q, r)
    return t == TURN_RIGHT or t == TURN_NONE and dist(r, p) < dist(q, p)


def gen(n=10, max_coord=100):
    pts = set()
    for i in range(2 * n):
        pts.add((rnd.randint(0, max_coord) + 1, rnd.randint(0, max_coord) + 1))
    res = list(map(lambda pt: [pt[0], pt[1]], list(pts)))
    return res[:min(len(res), n)]


def is_convex(pts):
    n = len(pts)
    for i in range(n):
        if turn(pts[i - 1], pts[i], pts[i + 1 - n]) == TURN_RIGHT:
            return False
    return True


def visualize(pts, hull):
    fig, ax = plt.subplots()
    ax.scatter([p[0] for p in pts], [p[1] for p in pts])
    ax.plot([h[0] for h in hull], [h[1] for h in hull], 'go-')
    plt.show()
