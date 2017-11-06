from cg.utils import cmp_

TURN_LEFT, TURN_RIGHT, TURN_NONE = (1, -1, 0)


def turn(p, q, r):
    # предикат поворота, возвращает 1, -1, 0, если точки p, q, r  образуют левый, правый повороты
    # или лежат на одной прямой, соответственно.
    return cmp_((q[0] - p[0]) * (r[1] - p[1]) - (r[0] - p[0]) * (q[1] - p[1]), 0)


def dist(q, p):
    # считаем квадрат расстояния
    dx, dy = q[0] - p[0], q[1] - p[1]
    return dx * dx + dy * dy


# верно ли, что r имеет меньший угол относительно p чем q или такой же,
# но удалена на меньшее расстояние от p
def angle_less(p, q, r):
    t = turn(p, q, r)
    return t == TURN_RIGHT or t == TURN_NONE and dist(r, p) < dist(q, p)
