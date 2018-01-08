import math
import time
from utils import *
from andrew import andrew_hull
import numpy as np

def int_log(n):
    return int(math.floor(math.log2(n)))


def fast_log(n):
    l, r = 0, n
    while l + 1 != r:
        m = (l + r) // 2
        if (1 << m) > n:
            r = m
        else:
            l = m
    return l


def measure(n):
    begin = time.time()
    log = int_log(n)
    end = time.time()
    print('float log ', end - begin)
    print(log)
    begin = time.time()
    a_log = fast_log(n)
    end = time.time()
    assert a_log == log
    print('binsearch log ', end - begin)


def r_tangent(hull, p):
    n = len(hull)
    log = int_log(n)
    step = 1 << max(log - 2, 0)
    res = 0
    for cur in range(0, n, step):
        if (turn(p, hull[cur], hull[cur - step]) != TURN_RIGHT) and \
                (turn(p, hull[cur], hull[cur + step - n]) != TURN_RIGHT):
            res = cur
    while step > 0:
        step >>= 1
        if turn(p, hull[res], hull[res + step - n]) == TURN_RIGHT:
            res = (res + step) % n
        elif turn(p, hull[res], hull[res - step]) == TURN_RIGHT:
            res = (res - step) % n
    assert turn(p, hull[res], hull[res + 1 - n]) != TURN_RIGHT and turn(p, hull[res], hull[res - 1]) != TURN_RIGHT
    return res


tests = [
    ([[0, 1], [1, 0], [2, 1], [2, 2], [1, 2]], [3, 1])
    , ([[0, 1], [1, 0], [2, 0], [3, 1], [3, 2], [2, 3], [1, 3], [0, 2]], [5, 2])
    , ([[0, 1], [1, 0], [2, 0], [3, 1], [3, 2], [2, 3], [1, 3], [0, 2]], [4, 0])
]

for i in range(100):
    max_coord = 10000
    ps = gen(1000, max_coord)
    hull = andrew_hull(ps)
    tests.append((hull, [max_coord + np.random.randint(0, max_coord) + 1, max_coord + np.random.randint(0, max_coord) + 1]))


def is_tangent(h, q, ind):
    n = len(h)
    for i in range(n):
        if turn(q, h[ind], h[i]) == TURN_RIGHT:
            return False
    return True


for (h, p) in tests:
    ind = r_tangent(h, p)
    print(h, p, h[ind], sep=' ')
    assert is_tangent(h, p, ind)
