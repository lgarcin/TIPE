import numpy as np
import matplotlib.pyplot as plt

j = np.exp(1j * np.pi / 3)


def koch(z1, z2):
    a = (z2 - z1) / 3
    return [z1, z1 + a, z1 + a + a / j * np.exp(1j * np.random.uniform(-1, 1)) * np.random.uniform(.5, 2), z1 + 2 * a]


def koch(z1, z2):
    a = (z2 - z1) / 3
    return [z1, z1 + a, z1 + a + a / j, z1 + 2 * a]


def koch_list(l):
    return np.concatenate([koch(z1, z2) for (z1, z2) in zip(l, np.roll(l, -1))])


def trace(n):
    plt.axis('equal')
    init = np.array([1, j ** 2, j ** 4])
    for k in range(n):
        plt.fill(init.real, init.imag, zorder=n - k)
        init = koch_list(init)
    plt.show()


trace(9)
