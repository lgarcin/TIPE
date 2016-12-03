from numpy import zeros, meshgrid, roll, concatenate, sqrt, ndarray, unravel_index
from numpy.random import normal, randint
from matplotlib import cm
from matplotlib.pyplot import matshow, show, figure, get_cmap, plot
from mpl_toolkits.mplot3d.axes3d import Axes3D
from pprint import pprint

n = 6
a = zeros((2 ** n, 2 ** n))
loc = 0
scale = 50
size = 2 ** n

while size > 1:
    sub = a[::size, ::size]
    shape = sub.shape
    noise = normal(loc, scale, shape)
    a[size // 2::size, size // 2::size] = (sub + roll(sub, -1, 0) + roll(sub, -1, 1) + roll(roll(sub, -1, 0), -1,
                                                                                            1)) / 4 + noise
    sub1 = a[::size, ::size]
    sub2 = a[size // 2::size, size // 2::size]
    noise = normal(loc, scale, shape)
    a[size // 2::size, ::size] = (sub1 + roll(sub1, -1, 0) + sub2 + roll(sub2, 1, 1)) / 4 + noise
    noise = normal(loc, scale, shape)
    a[::size, size // 2::size] = (sub1 + roll(sub1, -1, 1) + sub2 + roll(sub2, 1, 0)) / 4 + noise
    # pprint(a)
    size //= 2
    scale /= 2

x, y = meshgrid(range(0, a.shape[0]), range(0, a.shape[1]))
ax = Axes3D(figure())
ax.plot_surface(x, y, a, rstride=1, cstride=1, cmap=get_cmap('terrain'), linewidth=1, antialiased=True)

i0, j0 = randint(0, a.shape[0]), randint(0, a.shape[1])
i1, j1 = randint(0, a.shape[0]), randint(0, a.shape[1])
i0, j0 = 0, 0
i1, j1 = a.shape[0] - 1, a.shape[1] - 1

d = ndarray(a.shape)
d.fill(float('inf'))
v = ndarray(a.shape)
v.fill(False)
p = ndarray((a.shape[0], a.shape[1], 2), dtype=int)
p.fill(-1)

d[i0, j0] = 0

while not v.all():
    dd = d.copy()
    for ii in range(a.shape[0]):
        for jj in range(a.shape[1]):
            if v[ii, jj]:
                dd[ii, jj] = float('inf')

    i, j = unravel_index(dd.argmin(), d.shape)
    if i == i1 and j == j1:
        break
    v[i, j] = True
    neighbours = []
    if i > 0:
        neighbours.append((i - 1, j))
    if i < a.shape[0] - 1:
        neighbours.append((i + 1, j))
    if j > 0:
        neighbours.append((i, j - 1))
    if j < a.shape[1] - 1:
        neighbours.append((i, j + 1))
    for ii, jj in neighbours:
        if not v[ii, jj]:
            alt = d[i, j] + sqrt(1 + (a[i, j] - a[ii, jj]) ** 2)
            if alt < d[ii, jj]:
                d[ii, jj] = alt
            p[ii, jj, :] = [i, j]

print(i0, j0, i1, j1)

i = i1
j = j1
x = []
y = []
z = []
while i != -1 and j != -1:
    x.append(j)
    y.append(i)
    z.append(a[i, j])
    i, j = p[i, j, 0], p[i, j, 1]

ax.plot(x, y, z)

matshow(a, cmap=get_cmap('terrain'))
plot(x, y)
show()
