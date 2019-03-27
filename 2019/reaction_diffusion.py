import numpy as np
import matplotlib.pyplot as plt


def laplacien(x):
    return np.roll(x, 1) + np.roll(x, -1) - 2 * x


n = 512

mu = .1
rho0 = .004
sigma = np.linspace(0.012, 0.038, n)
nu = 0
Da = .1
Ds = .1
kappa = 1
rho = .5


def evol(a, s, dt, N):
    la = [a.copy()]
    ls = [s.copy()]
    for n in range(N):
        a2 = a ** 2 / (1 + kappa * a ** 2) + rho0
        da = rho * s * a2 - mu * a + Da * laplacien(a)
        ds = sigma - rho * s * a2 - nu * s + Ds * laplacien(s)
        a += da * dt
        s += ds * dt
        if n % 10 == 0:
            la.append(a.copy())
            ls.append(s.copy())
    return la, ls


a = np.ones(n) * 0
s = np.ones(n) * 0
la, ls = evol(a, s, 1, 10000)

plt.imshow(la, cmap='gray')
plt.show()

# plt.imshow(ls, cmap='gray')
# plt.show()
