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
    cnt_left, cnt_right = 0, 0
    for i in range(n):
        t = turn(pts[i - 1], pts[i], pts[i + 1 - n])
        if t == TURN_RIGHT:
            cnt_right += 1
        elif t == TURN_LEFT:
            cnt_left += 1
            # print(pts[i - 1])
            # print(pts[i])
            # print(pts[i + 1 - n])
            # return False
    return cnt_left == 0 or cnt_right == 0


def is_in_triangle(a, b, c, point):
    # return abs(turn(a, b, point) + turn(b, c, point) + turn(c, a, point)) == 3
    return is_in_polygon([a, b, c], point)


def is_in_polygon(poly, point):
    cnt_left, cnt_right = 0, 0
    n = len(poly)
    for i in range(n):
        t = turn(poly[i], poly[i + 1 - n], point)
        if t == TURN_LEFT:
            cnt_left += 1
        elif t == TURN_RIGHT:
            cnt_right += 1
    return cnt_left == 0 or cnt_right == 0


def visualize(pts, hull, marked=[]):
    fig, ax = plt.subplots()
    ax.scatter([p[0] for p in pts], [p[1] for p in pts])
    ax.plot([h[0] for h in hull] + ([hull[0][0]] if hull else []),
            [h[1] for h in hull] + ([hull[0][1]] if hull else []), 'go-')
    ax.plot([m[0] for m in marked], [m[1] for m in marked], 'ro', lw=0)
    plt.show()
