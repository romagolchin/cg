import matplotlib.pyplot as plt

example_melkman = []
example_melkman.append([
    [5.0, 0.0],
    [5.0, 1.0],
    [7.0, 3.0],
    [4.0, 4.0],
    [4.5, 3.0],
    [1.0, 7.0]
])
example_melkman.append([
    [1., 1.],
    [3., 3.],
    [4., 1.1],
    [5.3, 1.0],
    [6.6, 1.5],
    [7.0, 3.0],
    [7.0, 5.0],
    [8.0, 5.0],
    [7.0, 1.0],
    [10.0, 1.0],
    [11.0, 5.8],
    [9.5, 6.5],
    [8.0, 8.0],
    [9.0, 2.2],
    [8.0, 6.0],
    [5.0, 6.0],
    [5.0, 9.5],
    [4.0, 5.5],
    [1.0, 9.5]
])

example_melkman.append([
    [1, 3],
    [3, 3],
    [5, 3],
    [4, 1]
])

example_melkman.append([
    [1., 1.],
    [2., 1.],
    [2., 2.],
    [1., 9.],
    [1.5, 8.],
    [2., 8.],
    [9., 9.],
    [9., 1.]
])


def plot_melkman(points, ans):
    plt.axis([0, 15, -1, 10])
    points_xs = [x[0] for x in points]
    points_ys = [y[1] for y in points]
    plt.plot(points_xs, points_ys, 'o-', color='black', linewidth=2)

    ans_xs = [x[0] for x in ans]
    ans_ys = [x[1] for x in ans]
    plt.plot(ans_xs, ans_ys, '-', color='#00ff00', linewidth=3)
    plt.plot(ans_xs, ans_ys, 'o', color='red', markersize=8)

    plt.show()


# plot_melkman(example_melkman[0], example_melkman[0])
