from utils import *
import qhull
from numpy import random as rnd


def get_hull_points(points):
    if len(points) < 2:
        return points
    min_pt, max_pt = get_min_max_x(points)
    left_of_line_pts, _, right_of_line_pts = split_by_line(min_pt, max_pt, points)
    return random_quick_hull(left_of_line_pts, min_pt, max_pt) + random_quick_hull(right_of_line_pts, max_pt, min_pt)


def split_by_line(start, end, points):
    left = []
    none = []
    right = []
    for pt in points:
        pt_turn = turn(start, end, pt)
        if pt_turn == TURN_LEFT:
            left.append(pt)
        elif pt_turn == TURN_RIGHT:
            right.append(pt)
        elif pt_turn == TURN_NONE:
            none.append(pt)
    return left, none, right


def point_max_from_line(start, end, points):
    max_dist = -1
    max_point = None
    for point in points:
        # if point != start and point != end:
        dist = distance(start, end, point)
        if dist > max_dist:
            max_dist = dist
            max_point = point

    return max_point


def split_by_two_lines(points, start, pivot, end):
    first, second = [], []
    for p in points:
        if p != start and p != pivot and p != end:
            if turn(start, pivot, p) != TURN_RIGHT:
                first.append(p)
            elif turn(pivot, end, p) != TURN_RIGHT:
                second.append(p)
    return first, second


def random_match(n):
    if n < 0:
        raise ValueError("negative integer passed: ", n)
    indices = list(range(n))
    result = []
    if n % 2 == 1:
        single = rnd.randint(0, n)
        indices.pop(single)
    while indices:
        match = rnd.randint(0, len(indices) - 1)
        result.append((indices.pop(), indices.pop(match)))
    return result


def random_quick_hull(points, start, end):
    if not points:
        return [end]
    n = len(points)
    index_1 = rnd.randint(0, n)
    if n == 1:
        pivot = points[0]
    else:
        index_2 = rnd.randint(0, n - 1)
        if index_2 >= index_1:
            index_2 += 1
        if is_in_triangle(start, end, points[index_1], points[index_2]):
            return random_quick_hull(points[:index_2] + points[index_2 + 1:], start, end)
        if is_in_triangle(start, end, points[index_2], points[index_1]):
            return random_quick_hull(points[:index_1] + points[index_1 + 1:], start, end)
        q_1 = points[index_1]
        q_2 = points[index_2]
        split = split_by_line(q_1, q_2, points)
        start_end_side = turn(q_1, q_2, start)
        if start_end_side == TURN_NONE:
            start_end_side = turn(q_1, q_2, end)
        if start_end_side == TURN_LEFT:
            opposite = split[2]
        elif start_end_side == TURN_RIGHT:
            opposite = split[0]
        else:
            raise AssertionError
        pivot = point_max_from_line(q_1, q_2, opposite + split[1])
    if pivot is None:
        return [end]
    for (first_index, second_index) in random_match(n):
        first_hull = qhull.get_hull_points([start, end, points[first_index], pivot])
        second_hull = qhull.get_hull_points([start, end, points[second_index], pivot])
        if is_in_polygon(first_hull, points[second_index]):
            points[second_index] = None
        if is_in_polygon(second_hull, points[first_index]):
            points[first_index] = None
    i = 0
    while i < len(points):
        if points[i] is None:
            points.pop(i)
            # print('pop')
        else:
            i += 1
    partition = split_by_two_lines(points, start, pivot, end)
    return random_quick_hull(partition[1], pivot, end) + random_quick_hull(partition[0], start, pivot)


def get_points_left_of_line(start, end, points):
    return split_by_line(start, end, points)[0]


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


def distance(start, end, pt):
    return abs(turn_value(start, end, pt))


# test = gen(n=100, max_coord=1000)
# test = [[0, 0],  [2, 10], [1, 1], [0, 3]]
# test = [[0, 0], [0, 3], [2, 0], [1, 2]]
# test = [[2, 7], [2, 6], [2, 3], [1, 6], [3, 6]]
# test = [[0, 0], [1, 1], [0, 2], [2, 0]]
# test = [[0, 0], [1, 1]]
# test = [[j, j] for j in range(10)]
# visualize(test, [])
# hull = get_hull_points(test)
# print(hull)
# visualize(test, hull)

# print(random_quick_hull([[0, 1], [0, 2]], [0, 0], [2, 0]))

f = True
for i in range(10000):
    if f:
        if i > 0 and i % 100 == 0:
            print(i)
        test = gen(n=100, max_coord=1000)
        hull = get_hull_points(test)
        # visualize(test, hull)
        if not is_convex(hull):
            print('not convex')
            print(test)
            visualize(test, hull)
            f = False
            break
        marked = []
        for t in test:
            if not is_in_polygon(hull, t):
                marked.append(t)
                f = False
        if marked:
            print('not hull')
            print(test)
            visualize(test, hull, marked)


