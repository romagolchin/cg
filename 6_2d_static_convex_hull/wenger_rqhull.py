from utils import *
from numpy import random as rnd


def get_hull_points(list_pts):
    min_pt, max_pt = get_min_max_x(list_pts)
    left_of_line_pts, right_of_line_pts = split_by_line(min_pt, max_pt, list_pts)
    hull_pts = random_quick_hull(left_of_line_pts, min_pt, max_pt)
    return hull_pts + random_quick_hull(right_of_line_pts, max_pt, min_pt)


def split_by_line(start, end, points):
    left = []
    right = []
    for pt in points:
        pt_turn = turn(start, end, pt)
        if pt_turn == TURN_LEFT:
            left.append(pt)
        elif pt_turn == TURN_RIGHT:
            right.append(pt)
    return left, right


def point_max_from_line(start, end, points):
    max_dist = 0
    max_point = None
    for point in points:
        if point != start and point != end:
            dist = distance(start, end, point)
            if dist > max_dist:
                max_dist = dist
                max_point = point

    return max_point


def split_by_two_lines(points, start, pivot, end):
    first, second = [], []
    for p in points:
        if turn(start, pivot, p) == TURN_LEFT:
            first.append(p)
        elif turn(start, pivot, p) == TURN_RIGHT and turn(pivot, end, p) == TURN_LEFT:
            second.append(p)
    return first, second


def random_quick_hull(points, start, end):
    if not points:
        return [end]
    index_1 = rnd.randint(0, len(points))
    if len(points) == 1:
        pivot = points[0]
    else:
        index_2 = rnd.randint(0, len(points) - 1)
        if index_2 >= index_1:
            index_2 += 1
        if is_in_triangle(start, end, points[index_1], points[index_2]):
            return random_quick_hull(points[:index_2] + points[index_2 + 1:], start, end)
        if is_in_triangle(start, end, points[index_2], points[index_1]):
            return random_quick_hull(points[:index_1] + points[index_1 + 1:], start, end)
        q_1 = points[index_1]
        q_2 = points[index_2]
        split = split_by_line(q_1, q_2, points)
        opposite = split[0] if turn(q_1, q_2, start) != TURN_LEFT else split[1]
        pivot = point_max_from_line(q_1, q_2, opposite)
    if pivot is None:
        return [end]
    partition = split_by_two_lines(points, start, pivot, end)
    return random_quick_hull(partition[0], start, pivot) + random_quick_hull(partition[1], pivot, end)


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


test = gen(n=100, max_coord=1000)
visualize(test, get_hull_points(test))
