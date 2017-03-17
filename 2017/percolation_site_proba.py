from dask.array.creation import linspace
from numpy.random import random
from numpy import ndarray, logical_and, array_equal, arange, mean, linspace
from scipy.ndimage.morphology import binary_dilation

N = 256
nb = 100


def success(p, N):
    grid = random((N, N)) < p
    access = ndarray((N, N))
    access.fill(False)
    a = access.copy()

    a[0, :] = grid[0, :]

    while not array_equal(access, a):
        access = a.copy()
        a = logical_and(binary_dilation(a), grid)

    return a[-1, :].any()


for p in linspace(0.55, .65, 11):
    print(p, mean([success(p, N) for _ in range(nb)]))
