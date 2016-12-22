from numpy.random import random, randint
from numpy import ndarray, logical_and, array_equal, where
from matplotlib.pyplot import show, axis, subplot, figure, axes
from scipy.ndimage.morphology import binary_dilation
from matplotlib.animation import ArtistAnimation, writers
from matplotlib.collections import LineCollection

N = 100
p = .57

grid = random((N, N)) < p
access = ndarray((N, N))
access.fill(False)
a = access.copy()

# x, y = where(grid)
# n = randint(len(x))
# i, j = x[n], y[n]
# a[i, j] = grid[i, j]

a[:, -1] = grid[:, -1]

ims = []
fig = figure()
ax = subplot()
axis('off')

while not array_equal(access, a):
    access = a.copy()
    a = logical_and(binary_dilation(a), grid)
    lines, colors = [], []
    for i in range(N - 1):
        for j in range(N):
            if access[i, j] and access[i + 1, j]:
                lines.append([(i, j), (i + 1, j)])
                colors.append([1, 0, 0, 1])
            elif grid[i, j] and grid[i + 1, j]:
                lines.append([(i, j), (i + 1, j)])
                colors.append([0, 0, 1, 1])
    for i in range(N):
        for j in range(N - 1):
            if access[i, j] and access[i, j + 1]:
                lines.append([(i, j), (i, j + 1)])
                colors.append([1, 0, 0, 1])
            elif grid[i, j] and grid[i, j + 1]:
                lines.append([(i, j), (i, j + 1)])
                colors.append([0, 0, 1, 1])
    ax.autoscale()
    ax.set_aspect('equal')
    ims.append([ax.add_collection(LineCollection(lines, colors=colors))])

ani = ArtistAnimation(fig, ims, interval=10, blit=True, repeat_delay=1000)
Writer = writers['ffmpeg']
writer = Writer(fps=10, metadata=dict(artist='Laurent Garcin'), bitrate=18000)
ani.save('perco_bond.mp4', writer=writer)
show()
