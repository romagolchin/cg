import numpy.random as rnd


def gen(n=7, max_coord=10):
    pts = set()
    for i in range(n):
        pts.add((rnd.randint(0, max_coord) + 1, rnd.randint(0, max_coord) + 1))
    return list(map(lambda pt: [pt[0], pt[1]], list(pts)))
