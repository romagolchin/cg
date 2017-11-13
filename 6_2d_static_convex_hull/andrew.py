from functools import reduce
from utils import *


def keep_left(hull, r):
    while len(hull) > 1 and turn(hull[-1], r, hull[-2]) != TURN_LEFT:
        hull.pop()
    if not len(hull) or hull[-1] != r:
        hull.append(r)
    return hull


def andrew_hull(points):
    points = sorted(points)
    lower_hull = reduce(keep_left, points, [])
    upper_hull = reduce(keep_left, reversed(points), [])
    return lower_hull.extend(upper_hull[i] for i in range(1, len(upper_hull) - 1)) or lower_hull
